"""Contains the software coordinating the logic of the application."""
import logging
import os
import sys
import traceback
import time
from PyQt5.QtCore import QObject, QThreadPool, QRunnable, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from download_dataset import DatasetController
from DicomToDatabase.dicom_to_db import dicom_to_db
from calculate_features import calculate_features
from LabelImages import LabelImageApplication
import DicomToDatabase.basic_db_ops as bdo
import DicomToDatabase.config as config
from classification import classification
from main_gui import MainApplication

SOURCE_URL = {
        'subset': 'https://github.com/Matt-Conrad/CXR_View_Classification/raw/master/NLMCXR_subset_dataset.tgz',
        'full_set': 'https://openi.nlm.nih.gov/imgs/collections/NLMCXR_dcm.tgz'
    }

def run_app():
    """Run the application that guides the user through the process."""
    app = QApplication(sys.argv)
    cont = Controller()
    app.exec_()

class Controller():
    """Controller class that controls the logic of the application."""
    def __init__(self):
        logging.info('***INITIALIZING CONTROLLER***')

        # String variables
        self.config_file_name = 'config.ini'
        self.dataset = config.config(filename=self.config_file_name, section='dataset_info')['dataset']
        self.url = SOURCE_URL[self.dataset]

        # Object variables
        self.main_app = MainApplication()
        self.label_app = None
        self.classifier = None
        self.dataset_controller = DatasetController(self.url)

        # From config file
        self.db_name = config.config(filename=self.config_file_name, section='postgresql')['database']
        self.meta_table_name = config.config(filename=self.config_file_name, section='table_info')['metadata_table_name']
        self.feat_table_name = config.config(filename=self.config_file_name, section='table_info')['features_table_name']
        self.label_table_name = config.config(filename=self.config_file_name, section='table_info')['label_table_name']

        # Set up the GUI
        self.init_gui_state()
        self.connect_buttons()
        self.threadpool = QThreadPool()
        logging.info('***CONTROLLER INITIALIZED***')

    ### DOWNLOAD BUTTON
    def download_dataset(self):
        """Delegate the downloading and GUI updating to 2 new threads."""
        logging.info('***BEGIN DOWNLOADING PHASE***')
        # Set the progress region
        self.main_app.msg_box.setText('Downloading images')
        self.main_app.pro_bar.setMinimum(0)
        self.main_app.pro_bar.setMaximum(self.get_tgz_max())
        
        # Create 2 workers: 1 to download and 1 to update the progress bar
        worker = Worker(self.download)
        updater = Worker(self.update)
        # Connect the updater signal to the progress bar
        updater.signals.progress.connect(self.main_app.update_pro_bar)
        updater.signals.finished.connect(self.main_app.update_text)
        # Start the threads
        self.threadpool.start(worker)
        self.threadpool.start(updater)

    def download(self, progress_callback, finished_callback):
        """Download the image set.
        
        Parameters
        ----------
        progress_callback : pyqtSignal(int)
            Passed automatically by Worker class, so does nothing in this function
        """
        self.dataset_controller.get_dataset()
        config.update_config_file(self.config_file_name, 'dicom_folder', 'folder_path', self.dataset_controller.folder_full_path)

    def update(self, progress_callback, finished_callback):
        """Updates the GUI's progress bar.

        Parameters
        ----------
        progress_callback : pyqtSignal(int)
            Used to emit a signal to the progress bar. Passed automatically by Worker class.
        """
        # Wait for the file to start downloading before updating progress bar
        while not os.path.exists(self.dataset_controller.filename_fullpath):
            pass

        # Update the progress bar with the current file size
        progress_callback.emit(0)
        self.log_gui_state('debug')
        while self.get_tgz_size() < self.get_tgz_max():
            progress_callback.emit(self.get_tgz_size())
            self.log_gui_state('debug')
            time.sleep(1)
        progress_callback.emit(self.get_tgz_size())

        # Update the text and move to the next stage
        finished_callback.emit('Image download complete')
        self.log_gui_state('debug')
        logging.info('***END DOWNLOADING PHASE***')
        self.main_app.stage2_ui()

    def get_tgz_size(self):
        """Calculates the size of the TGZ file for the purpose of setting the progress bar value."""
        if self.dataset == 'full_set':
            # Dividing by 100 because the expected size of this TGZ is larger than QProgressBar accepts
            return int(os.path.getsize(self.dataset_controller.filename_fullpath) / 100)
        elif self.dataset == 'subset':
            return os.path.getsize(self.dataset_controller.filename_fullpath)
        else:
            raise ValueError('Value must be one of the keys in SOURCE_URL')

    def get_tgz_max(self):
        """Calculates the size of the TGZ file max for the purpose of setting the progress bar max."""
        if self.dataset == 'full_set':
            # Dividing by 100 because the expected size of this TGZ is larger than QProgressBar accepts
            return int(self.dataset_controller.expected_size / 100)
        elif self.dataset == 'subset':
            return self.dataset_controller.expected_size
        else:
            raise ValueError('Value must be one of the keys in SOURCE_URL')

    ### UNPACK BUTTON
    def unpack_dataset(self):
        """Delegate the unpacking and GUI updating to 2 new threads."""
        logging.info('***BEGIN UNPACKING PHASE***')
        # Set the progress region
        self.main_app.msg_box.setText('Unpacking images')
        self.main_app.pro_bar.setMinimum(0)
        self.main_app.pro_bar.setMaximum(self.dataset_controller.expected_num_files)

        # Create 2 workers: 1 to unpack and 1 to update the progress bar
        worker = Worker(self.unpack)
        updater = Worker(self.update_unpack)
        # Connect the updater signal to the progress bar
        updater.signals.progress.connect(self.main_app.update_pro_bar)
        updater.signals.finished.connect(self.main_app.update_text)
        # Start the threads
        self.threadpool.start(worker)
        self.threadpool.start(updater)

    def unpack(self, progress_callback, finished_callback):
        """Unpack the image set.
        
        Parameters
        ----------
        progress_callback : pyqtSignal(int)
            Passed automatically by Worker class, so does nothing in this function
        """
        self.dataset_controller.unpack()

    def update_unpack(self, progress_callback, finished_callback):
        """Updates the GUI's progress bar.

        Parameters
        ----------
        progress_callback : pyqtSignal(int)
            Used to emit a signal to the progress bar. Passed automatically by Worker class.
        """
        # Wait for the folder to be available before updating progress bar
        while not os.path.isdir(self.dataset_controller.folder_full_path):
            logging.debug('waiting')
            time.sleep(1)
            pass

        # Update the progress bar with the current file count in the folder path
        progress_callback.emit(0)
        self.log_gui_state('debug')
        while self.count_DCMs(self.dataset_controller.folder_full_path) < self.dataset_controller.expected_num_files:
            progress_callback.emit(self.count_DCMs(self.dataset_controller.folder_full_path))
            self.log_gui_state('debug')
            time.sleep(1)
        progress_callback.emit(self.count_DCMs(self.dataset_controller.folder_full_path))
        logging.debug('Final count: ' + str(self.count_DCMs(self.dataset_controller.folder_full_path)))

        # Update the text and move to the next stage
        finished_callback.emit('Images unpacked')
        self.log_gui_state('debug')
        logging.info('***END UNPACKING PHASE***')
        self.main_app.stage3_ui()

    def count_DCMs(self, full_folder_path):
        return sum([len(files) for r, d, files in os.walk(full_folder_path) if any(item.endswith('.dcm') for item in files)])

    ### STORE BUTTON
    def store_metadata(self):
        """Delegate the storing of metadata and GUI updating to 2 new threads."""
        logging.info('***BEGIN STORING PHASE***')
        # Set the progress region
        self.main_app.msg_box.setText('Storing metadata')
        self.main_app.pro_bar.setMinimum(0)
        self.main_app.pro_bar.setMaximum(self.dataset_controller.expected_num_files)

        # Create 2 workers: 1 to store and 1 to update the progress bar
        worker = Worker(self.to_db, self.dataset_controller.columns_info_full_path, self.config_file_name, 'elements')
        updater = Worker(self.update_store)
        # Connect the updater signal to the progress bar
        updater.signals.progress.connect(self.main_app.update_pro_bar)
        updater.signals.finished.connect(self.main_app.update_text)
        # Start the threads
        self.threadpool.start(worker)
        self.threadpool.start(updater)

    def to_db(self, columns_info, config_file_name, section_name, progress_callback, finished_callback):
        """Store the metadata from the folder to Postgres.
        
        Parameters
        ----------
        columns_info : string
            The name of the JSON containing the column info of the DB table
        config_file_name : string
            The name of the INI config file containing DB info and folder locations
        section_name : string
            The name corresponding to the section of the columns_info to use
        progress_callback : pyqtSignal(int)
            Passed automatically by Worker class, so does nothing in this function
        """
        dicom_to_db(columns_info, config_file_name, section_name)

    def update_store(self, progress_callback, finished_callback):
        """Updates the GUI's progress bar.

        Parameters
        ----------
        progress_callback : pyqtSignal(int)
            Used to emit a signal to the progress bar. Passed automatically by Worker class.
        """
        # Wait for the table to be available before updating progress bar
        while not bdo.table_exists(self.config_file_name, self.db_name, self.meta_table_name):
            pass
            
        # Update the progress bar with the current record count in the DB table
        progress_callback.emit(0)
        self.log_gui_state('debug')
        while bdo.count_records(self.config_file_name, self.db_name, self.meta_table_name) < self.dataset_controller.expected_num_files:
            progress_callback.emit(bdo.count_records(self.config_file_name, self.db_name, self.meta_table_name))
            self.log_gui_state('debug')
            time.sleep(1)
        progress_callback.emit(bdo.count_records(self.config_file_name, self.db_name, self.meta_table_name))
        
        # Update the text and move to the next stage
        finished_callback.emit('Done storing metadata')
        self.log_gui_state('debug')
        logging.info('***END STORING PHASE***')
        self.main_app.stage4_ui()

    ### CALCULATE BUTTON
    def calculate_features(self):
        """Delegate the feature calculating and GUI updating to 2 new threads."""
        logging.info('***BEGIN FEATURE CALCULATION PHASE***')
        # Set the progress region
        self.main_app.msg_box.setText('Calculating features')
        self.main_app.pro_bar.setMinimum(0)
        self.main_app.pro_bar.setMaximum(self.dataset_controller.expected_num_files)

        # Add table to DB
        bdo.add_table_to_db(self.feat_table_name, self.dataset_controller.columns_info_full_path, self.config_file_name, 'features_list')

        # Create 2 workers: 1 to calculate features and 1 to update the progress bar
        worker = Worker(self.calc_feat, self.config_file_name)
        updater = Worker(self.update_calc)
        # Connect the updater signal to the progress bar
        updater.signals.progress.connect(self.main_app.update_pro_bar)
        updater.signals.finished.connect(self.main_app.update_text)
        # Start the threads
        self.threadpool.start(worker)
        self.threadpool.start(updater)

    def calc_feat(self, config_file_name, progress_callback, finished_callback):
        """Calculate the features.
        
        Parameters
        ----------
        config_file_name : string
            The name of the INI config file containing DB info and folder locations
        progress_callback : pyqtSignal(int)
            Passed automatically by Worker class, so does nothing in this function
        """
        calculate_features(config_file_name)

    def update_calc(self, progress_callback, finished_callback):
        """Updates the GUI's progress bar.

        Parameters
        ----------
        progress_callback : pyqtSignal(int)
            Used to emit a signal to the progress bar. Passed automatically by Worker class.
        """
        # Wait for the table to be available before updating progress bar
        while not bdo.table_exists(self.config_file_name, self.db_name, self.feat_table_name):
            pass
        
        # Update the progress bar with the current record count in the DB table
        progress_callback.emit(0)
        while bdo.count_records(self.config_file_name, self.db_name, self.feat_table_name) < self.dataset_controller.expected_num_files:
            progress_callback.emit(bdo.count_records(self.config_file_name, self.db_name, self.feat_table_name))
            time.sleep(1)
        progress_callback.emit(bdo.count_records(self.config_file_name, self.db_name, self.feat_table_name))

        # Update the text and move to the next stage
        finished_callback.emit('Done calculating features')
        logging.info('***END FEATURE CALCULATION PHASE***')
        self.main_app.stage5_ui()

    ### LABEL BUTTON
    def label_images(self):
        """Use an app to manually label images."""
        logging.info('***BEGIN LABELING PHASE***')
        # Set the progress region
        self.main_app.pro_bar.setMinimum(0)
        self.main_app.pro_bar.setMaximum(self.dataset_controller.expected_num_files)
        if self.dataset == 'subset':
            # Set the progress region
            self.main_app.msg_box.setText('Please manually label images')
            
            # Add table to DB
            bdo.add_table_to_db(self.label_table_name, self.dataset_controller.columns_info_full_path, self.config_file_name, 'labels')

            # Create 1 thread to update the progress bar as the app runs
            updater = Worker(self.check_done)
            # Connect the updater signal to the progress bar
            updater.signals.progress.connect(self.main_app.update_pro_bar)
            updater.signals.finished.connect(self.main_app.update_text)
            # Start the thread
            self.threadpool.start(updater)

            # Open new window with the labeling app
            self.label_app = LabelImageApplication(self.config_file_name)
        elif self.dataset == 'full_set':
            bdo.import_image_label_data(self.label_table_name, self.dataset_controller.parent_folder + '/' + 'image_labels.csv', self.dataset_controller.columns_info_full_path, self.config_file_name, 'labels')
            logging.info('***END LABELING PHASE***')
            self.main_app.update_text('Done importing labels')
            self.main_app.update_pro_bar(self.dataset_controller.expected_num_files)
            self.main_app.stage6_ui()
        else:
            raise ValueError('Value must be one of the keys in SOURCE_URL')
        
    def check_done(self, progress_callback, finished_callback):
        """Updates the GUI's progress bar.

        Parameters
        ----------
        progress_callback : pyqtSignal(int)
            Passed automatically by Worker class, so does nothing in this function.
        """
        # Continually check for the number of records in the DB table
        progress_callback.emit(0)
        while bdo.count_records(self.config_file_name, self.db_name, self.label_table_name) < self.dataset_controller.expected_num_files:
            progress_callback.emit(bdo.count_records(self.config_file_name, self.db_name, self.label_table_name))
            time.sleep(1)
        progress_callback.emit(bdo.count_records(self.config_file_name, self.db_name, self.label_table_name))

        # Update the text and move to the next stage
        finished_callback.emit('Done labeling')
        logging.info('***END LABELING PHASE***')
        self.main_app.stage6_ui()

    ### CLASSIFICATION BUTTON
    def classification(self):
        """Performs the training of classifier and gets the accuracy of the classifier."""
        logging.info('***BEGIN CLASSIFICATION PHASE***')
        self.classifier, accuracy = classification(self.config_file_name)
        self.main_app.update_text('Accuracy: ' + str(accuracy))
        logging.info('***END CLASSIFICATION PHASE***')

    ### GUI HELPER FUNCTIONS
    def connect_buttons(self):
        """Connect the buttons in the GUI to the functions here."""
        self.main_app.download_btn.clicked.connect(self.download_dataset)
        self.main_app.unpack_btn.clicked.connect(self.unpack_dataset)
        self.main_app.store_btn.clicked.connect(self.store_metadata)
        self.main_app.features_btn.clicked.connect(self.calculate_features)
        self.main_app.label_btn.clicked.connect(self.label_images)
        self.main_app.classify_btn.clicked.connect(self.classification)

    def init_gui_state(self):
        """Initialize the GUI in the right stage."""
        # Set icon
        self.main_app.setWindowIcon(QIcon(self.dataset_controller.parent_folder + '/' + 'icon.jpg'))

        if not os.path.exists(self.dataset_controller.filename) and not os.path.isdir(self.dataset_controller.folder_name) and not bdo.table_exists(self.config_file_name, self.db_name, self.meta_table_name): # If the TGZ hasn't been downloaded
            self.main_app.stage1_ui()
        elif os.path.exists(self.dataset_controller.filename) and not os.path.isdir(self.dataset_controller.folder_name) and not bdo.table_exists(self.config_file_name, self.db_name, self.meta_table_name):
            self.main_app.stage2_ui()
        elif os.path.exists(self.dataset_controller.filename) and os.path.isdir(self.dataset_controller.folder_name) and not bdo.table_exists(self.config_file_name, self.db_name, self.meta_table_name):
            self.main_app.stage3_ui()
        elif os.path.exists(self.dataset_controller.filename) and os.path.isdir(self.dataset_controller.folder_name) and bdo.table_exists(self.config_file_name, self.db_name, self.meta_table_name) and not bdo.table_exists(self.config_file_name, self.db_name, self.feat_table_name):
            self.main_app.stage4_ui()
        elif os.path.exists(self.dataset_controller.filename) and os.path.isdir(self.dataset_controller.folder_name) and bdo.table_exists(self.config_file_name, self.db_name, self.feat_table_name) and bdo.table_exists(self.config_file_name, self.db_name, self.feat_table_name) and not bdo.table_exists(self.config_file_name, self.db_name, self.label_table_name):
            self.main_app.stage5_ui()
        elif os.path.exists(self.dataset_controller.filename) and os.path.isdir(self.dataset_controller.folder_name) and bdo.table_exists(self.config_file_name, self.db_name, self.feat_table_name) and bdo.table_exists(self.config_file_name, self.db_name, self.feat_table_name) and bdo.table_exists(self.config_file_name, self.db_name, self.feat_table_name):
            self.main_app.stage6_ui()

    def log_gui_state(self, debug_level):
        """Log the state of the feedback in the GUI."""
        if debug_level == 'debug':
            logging.debug('Text: ' + self.main_app.msg_box.text())
            logging.debug('Progress bar value: ' + str(self.main_app.pro_bar.value()))

class WorkerSignals(QObject):
    """Container class for signals used by the Worker class."""
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)

class Worker(QRunnable):
    """Flexible class that helps run threads.

    From https://www.learnpyqt.com/courses/concurrent-execution/multithreading-pyqt-applications-qthreadpool/
    """
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add the callback to our kwargs
        self.kwargs['progress_callback'] = self.signals.progress # Passes the progress signal to the function
        self.kwargs['finished_callback'] = self.signals.finished # Passes the finished signal to the function  

    @pyqtSlot()
    def run(self):
        """Initialise the runner function with passed args, kwargs."""
        # self.fn(*self.args, **self.kwargs)
        try:
            self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            print(exctype, value)

if __name__ == "__main__":
    # Get log level from config file
    log_level = config.config(filename='config.ini', section='logging')['level']
    if log_level == 'debug':
        log_level_obj = logging.DEBUG
    elif log_level == 'info':
        log_level_obj = logging.INFO
    
    # Remove any log handlers to make way for our logger
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    
    # Set the logging
    logging.basicConfig(filename='CXR_Classification.log', level=log_level_obj,
                        format='%(asctime)s %(levelname)-8s: %(message)s', datefmt='%Y-%m-%d|%H:%M:%S')

    # Run the application
    run_app()