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
        self.threadpool.start(worker)
        self.threadpool.start(updater)

    def download(self):
        self.dataset_controller.get_dataset()

    def update(self):
        """Download the dataset (tgz format) from the public repository."""
        while not os.path.exists(self.dataset_controller.filename):
            pass
        
        self.mainApp.pro_bar.setValue(0)
        while os.path.getsize(self.dataset_controller.filename) < self.dataset_controller.expected_size:
            self.mainApp.pro_bar.setValue(os.path.getsize(self.dataset_controller.filename))
            time.sleep(1)
        self.mainApp.pro_bar.setValue(os.path.getsize(self.dataset_controller.filename))
        self.mainApp.msg_box.setText('Image download complete')
        self.mainApp.stage2_ui()
            
    ### UNPACK BUTTON
    def unpack_dataset(self):
        self.mainApp.msg_box.setText('Unpacking images')
        self.mainApp.pro_bar.setMinimum(0)
        self.mainApp.pro_bar.setMaximum(self.dataset_controller.expected_num_files)

        worker = Worker(self.dataset_controller.unpack)
        updater = Worker(self.update_unpack)
        self.threadpool.start(worker)
        self.threadpool.start(updater)

    def update_unpack(self):
        self.mainApp.pro_bar.setValue(0)
        while sum([len(files) for r, d, files in os.walk(self.dataset_controller.folder_full_path)]) < self.dataset_controller.expected_num_files:
            num_files = sum([len(files) for r, d, files in os.walk(self.dataset_controller.folder_full_path)])
            self.mainApp.pro_bar.setValue(num_files)
        num_files = sum([len(files) for r, d, files in os.walk(self.dataset_controller.folder_full_path)])
        self.mainApp.pro_bar.setValue(num_files)
        self.mainApp.msg_box.setText('Images unpacked')
        self.mainApp.stage3_ui()
        
    ### STORE BUTTON
    def store_metadata(self, feedback_dashboard):
        """Move all desired DCM tag-values from a directory full of DCMs into a PostgreSQL DB."""
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            executor.submit(self.update_store, feedback_dashboard)
            executor.submit(dicom_to_db, self.columns_info, self.config_file_name, 'elements')
        dicom_to_db(self.columns_info, self.config_file_name, 'elements')

    def update_store(self, feedback_dashboard):
        while bdo.count_records(self.config_file_name) < self.dataset_controller.expected_num_files:
            feedback_dashboard.itemAt(1).widget().setValue(bdo.count_records(self.config_file_name))
        feedback_dashboard.itemAt(1).widget().setValue(bdo.count_records(self.config_file_name))

    def calculate_features(self):
        """Calculate features for each image in the Postgres DB."""
        table_name = config.get_config_setting(self.config_file_name, section='table_info', key='features_table_name')
        bdo.add_table_to_db(table_name, self.columns_info, self.config_file_name, 'features_list')
        calculate_features(self.config_file_name)

    def label_images(self):
        """Use an app to manually label images."""
        table_name = config.get_config_setting(self.config_file_name, section='table_info', key='label_table_name')
        bdo.add_table_to_db(table_name, self.columns_info, self.config_file_name, 'labels')
        self.label_app = LabelImageApplication(self.config_file_name)

    def classification(self):
        """Performs the classification and gets the accuracy of the classifier."""
        self.classifier, accuracy = classification(self.config_file_name)

    def connect_buttons(self):
        self.mainApp.download_btn.clicked.connect(self.download_dataset)
        self.mainApp.unpack_btn.clicked.connect(self.unpack_dataset)
        self.mainApp.store_btn.clicked.connect(self.store_metadata)
        # self.mainApp.features_btn.clicked.connect(self.controller.calculate_features)
        # self.mainApp.label_btn.clicked.connect(self.controller.label_images)
        # self.mainApp.classify_btn.clicked.connect(self.controller.classification)

    def init_gui_state(self):
        if not os.path.exists(self.dataset_controller.filename) and not os.path.isdir(self.dataset_controller.folder_name): # If the TGZ hasn't been downloaded
            self.mainApp.stage1_ui()
        elif os.path.exists(self.dataset_controller.filename) and not os.path.isdir(self.dataset_controller.folder_name):
            self.mainApp.stage2_ui()
        elif os.path.exists(self.dataset_controller.filename) and os.path.isdir(self.dataset_controller.folder_name):
            self.mainApp.stage3_ui()

class WorkerSignals(QObject):
    finished = pyqtSignal()

class Worker(QRunnable):
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals() 

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''
        self.fn(*self.args, **self.kwargs)

if __name__ == "__main__":
    run_app()