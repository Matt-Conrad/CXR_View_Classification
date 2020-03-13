"""Contains the software coordinating the logic of the application."""
import logging
import os
import sys
import concurrent.futures
from PyQt5.QtCore import QObject, QThreadPool, QRunnable, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QApplication
from download_dataset import DatasetController
from DicomToDatabase.dicom_to_db import dicom_to_db
from calculate_features import calculate_features
from LabelImages import LabelImageApplication
import DicomToDatabase.basic_db_ops as bdo
import DicomToDatabase.config as config
from classification import classification
from main_gui import MainApplication
import time

logging.basicConfig(filename='CXR_Classification.log', level=logging.INFO)

def run_app():
    """Run application that guides the user through the process."""
    app = QApplication(sys.argv)
    cont = Controller()
    sys.exit(app.exec_())

class Controller():
    """Controller class that controls the logic of the application."""
    def __init__(self):
        logging.info('Initializing Controller')
        self.mainApp = MainApplication()

        self.config_file_name = 'config.ini'
        self.columns_info = 'columns_info.json'
        self.label_app = None
        self.classifier = None
        # self.url = 'https://openi.nlm.nih.gov/imgs/collections/NLMCXR_dcm.tgz'
        self.url = 'https://github.com/Matt-Conrad/CXR_View_Classification/raw/master/NLMCXR_subset_dataset.tgz'
        self.dataset_controller = DatasetController(self.url)

        self.db_name = config.config(filename=self.config_file_name, section='postgresql')['database']
        self.meta_table_name = config.config(filename=self.config_file_name, section='table_info')['metadata_table_name']
        self.feat_table_name = config.config(filename=self.config_file_name, section='table_info')['features_table_name']
        self.label_table_name = config.config(filename=self.config_file_name, section='table_info')['label_table_name']

        self.init_gui_state()
        self.connect_buttons()

        self.threadpool = QThreadPool()
        logging.info('Controller initialized')

    ### DOWNLOAD BUTTON
    def download_dataset(self):
        self.mainApp.msg_box.setText('Downloading images')
        self.mainApp.pro_bar.setMinimum(0)
        self.mainApp.pro_bar.setMaximum(self.dataset_controller.expected_size)

        worker = Worker(self.download)
        updater = Worker(self.update)
        updater.signals.progress.connect(self.mainApp.pro_bar.setValue)
        self.threadpool.start(worker)
        self.threadpool.start(updater)

    def download(self, progress_callback):
        self.dataset_controller.get_dataset()

    def update(self, progress_callback):
        """Download the dataset (tgz format) from the public repository."""
        while not os.path.exists(self.dataset_controller.filename):
            pass

        progress_callback.emit(0)
        while os.path.getsize(self.dataset_controller.filename) < self.dataset_controller.expected_size:
            progress_callback.emit(os.path.getsize(self.dataset_controller.filename))
            time.sleep(1)
        progress_callback.emit(os.path.getsize(self.dataset_controller.filename))
        self.mainApp.msg_box.setText('Image download complete') # 
        self.mainApp.stage2_ui()
            
    ### UNPACK BUTTON
    def unpack_dataset(self):
        self.mainApp.msg_box.setText('Unpacking images')
        self.mainApp.pro_bar.setMinimum(0)
        self.mainApp.pro_bar.setMaximum(self.dataset_controller.expected_num_files)

        worker = Worker(self.unpack)
        updater = Worker(self.update_unpack)
        updater.signals.progress.connect(self.mainApp.pro_bar.setValue)
        self.threadpool.start(worker)
        self.threadpool.start(updater)

    def unpack(self, progress_callback):
        self.dataset_controller.unpack()

    def update_unpack(self, progress_callback):
        progress_callback.emit(0)
        while sum([len(files) for r, d, files in os.walk(self.dataset_controller.folder_full_path)]) < self.dataset_controller.expected_num_files:
            num_files = sum([len(files) for r, d, files in os.walk(self.dataset_controller.folder_full_path)])
            progress_callback.emit(num_files)
        num_files = sum([len(files) for r, d, files in os.walk(self.dataset_controller.folder_full_path)])
        progress_callback.emit(num_files)
        self.mainApp.msg_box.setText('Images unpacked')
        self.mainApp.stage3_ui()
        
    ### STORE BUTTON
    def store_metadata(self):
        self.mainApp.msg_box.setText('Storing metadata')
        self.mainApp.pro_bar.setMinimum(0)
        self.mainApp.pro_bar.setMaximum(self.dataset_controller.expected_num_files)

        worker = Worker(self.to_db, self.columns_info, self.config_file_name, 'elements')
        updater = Worker(self.update_store)
        updater.signals.progress.connect(self.mainApp.pro_bar.setValue)
        self.threadpool.start(worker)
        self.threadpool.start(updater)

    def to_db(self, columns_info, config_file_name, section_name, progress_callback):
        dicom_to_db(columns_info, config_file_name, section_name)

    def update_store(self, progress_callback):
        progress_callback.emit(0)
        while not bdo.table_exists(self.config_file_name, self.db_name, self.meta_table_name):
            pass

        while bdo.count_records(self.config_file_name, self.db_name, self.meta_table_name) < self.dataset_controller.expected_num_files:
            progress_callback.emit(bdo.count_records(self.config_file_name, self.db_name, self.meta_table_name))
        progress_callback.emit(bdo.count_records(self.config_file_name, self.db_name, self.meta_table_name))
        self.mainApp.msg_box.setText('Metadata stored')
        self.mainApp.stage4_ui()

    ### CALCULATE BUTTON
    def calculate_features(self):
        """Calculate features for each image in the Postgres DB."""
        self.mainApp.msg_box.setText('Calculating features')
        self.mainApp.pro_bar.setMinimum(0)
        self.mainApp.pro_bar.setMaximum(self.dataset_controller.expected_num_files)

        bdo.add_table_to_db(self.feat_table_name, self.columns_info, self.config_file_name, 'features_list')

        worker = Worker(self.calc_feat, self.config_file_name)
        updater = Worker(self.update_calc)
        updater.signals.progress.connect(self.mainApp.pro_bar.setValue)
        self.threadpool.start(worker)
        self.threadpool.start(updater)

    def calc_feat(self, config_file_name, progress_callback):
        calculate_features(config_file_name)

    def update_calc(self, progress_callback):
        progress_callback.emit(0)
        while not bdo.table_exists(self.config_file_name, self.db_name, self.feat_table_name):
            pass

        while bdo.count_records(self.config_file_name, self.db_name, self.feat_table_name) < self.dataset_controller.expected_num_files:
            progress_callback.emit(bdo.count_records(self.config_file_name, self.db_name, self.feat_table_name))
        progress_callback.emit(bdo.count_records(self.config_file_name, self.db_name, self.feat_table_name))
        self.mainApp.msg_box.setText('Features calculated')
        self.mainApp.stage5_ui()

    ### LABEL BUTTON
    def label_images(self):
        """Use an app to manually label images."""
        self.mainApp.msg_box.setText('Please manually label images')
        
        bdo.add_table_to_db(self.label_table_name, self.columns_info, self.config_file_name, 'labels')

        updater = Worker(self.check_done)
        updater.signals.progress.connect(self.mainApp.pro_bar.setValue)
        self.threadpool.start(updater)

        self.label_app = LabelImageApplication(self.config_file_name)
        
    def check_done(self, progress_callback):
        while bdo.count_records(self.config_file_name, self.db_name, self.label_table_name) < self.dataset_controller.expected_num_files:
            time.sleep(1)

        self.mainApp.msg_box.setText('Images successfully labeled')
        self.mainApp.stage6_ui()

    ### CLASSIFICATION BUTTON
    def classification(self):
        """Performs the classification and gets the accuracy of the classifier."""
        self.classifier, accuracy = classification(self.config_file_name)
        self.mainApp.msg_box.setText('Accuracy: ' + str(accuracy))

    def connect_buttons(self):
        self.mainApp.download_btn.clicked.connect(self.download_dataset)
        self.mainApp.unpack_btn.clicked.connect(self.unpack_dataset)
        self.mainApp.store_btn.clicked.connect(self.store_metadata)
        self.mainApp.features_btn.clicked.connect(self.calculate_features)
        self.mainApp.label_btn.clicked.connect(self.label_images)
        self.mainApp.classify_btn.clicked.connect(self.classification)

    def init_gui_state(self):
        if not os.path.exists(self.dataset_controller.filename) and not os.path.isdir(self.dataset_controller.folder_name) and not bdo.table_exists(self.config_file_name, self.db_name, self.meta_table_name): # If the TGZ hasn't been downloaded
            self.mainApp.stage1_ui()
        elif os.path.exists(self.dataset_controller.filename) and not os.path.isdir(self.dataset_controller.folder_name) and not bdo.table_exists(self.config_file_name, self.db_name, self.meta_table_name):
            self.mainApp.stage2_ui()
        elif os.path.exists(self.dataset_controller.filename) and os.path.isdir(self.dataset_controller.folder_name) and not bdo.table_exists(self.config_file_name, self.db_name, self.meta_table_name):
            self.mainApp.stage3_ui()
        elif os.path.exists(self.dataset_controller.filename) and os.path.isdir(self.dataset_controller.folder_name) and bdo.table_exists(self.config_file_name, self.db_name, self.meta_table_name) and not bdo.table_exists(self.config_file_name, self.db_name, self.feat_table_name):
            self.mainApp.stage4_ui()
        elif os.path.exists(self.dataset_controller.filename) and os.path.isdir(self.dataset_controller.folder_name) and bdo.table_exists(self.config_file_name, self.db_name, self.feat_table_name) and bdo.table_exists(self.config_file_name, self.db_name, self.feat_table_name) and not bdo.table_exists(self.config_file_name, self.db_name, self.label_table_name):
            self.mainApp.stage5_ui()
        elif os.path.exists(self.dataset_controller.filename) and os.path.isdir(self.dataset_controller.folder_name) and bdo.table_exists(self.config_file_name, self.db_name, self.feat_table_name) and bdo.table_exists(self.config_file_name, self.db_name, self.feat_table_name) and bdo.table_exists(self.config_file_name, self.db_name, self.feat_table_name):
            self.mainApp.stage6_ui()

class WorkerSignals(QObject):
    progress = pyqtSignal(int)

class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress # Passes the progress signal to the function  

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        self.fn(*self.args, **self.kwargs)

if __name__ == "__main__":
    run_app()