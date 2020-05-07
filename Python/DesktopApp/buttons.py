"""Contains the code for the buttons for the app GUI."""
import logging
import os
import time
from PyQt5.QtWidgets import QPushButton
from classification import classification
from calculate_features import calculate_features
from workers import Worker, Updater
import metadata_to_db.basic_db_ops as bdo
import metadata_to_db.config as config
from metadata_to_db.dicom_to_db import dicom_to_db
from LabelImages import LabelImageApplication

class DownloadButton(QPushButton):
    def __init__(self, text, window, controller):
        QPushButton.__init__(self, text, window)
        self.clicked.connect(self.download_dataset)
        self.controller = controller

    def download_dataset(self):
        """Delegate the downloading and GUI updating to 2 new threads."""
        logging.info('***BEGIN DOWNLOADING PHASE***')
        # Set the progress region
        self.controller.main_app.msg_box.setText('Downloading images')
        self.controller.main_app.pro_bar.setMinimum(0)
        self.controller.main_app.pro_bar.setMaximum(self.get_tgz_max())
        
        # Create 2 workers: 1 to download and 1 to update the progress bar
        worker = Worker(self.download)
        updater = Updater(self.update)
        # Connect the updater signal to the progress bar
        updater.signals.progress.connect(self.controller.main_app.update_pro_bar)
        updater.signals.finished.connect(self.controller.main_app.update_text)
        # Start the threads
        self.controller.threadpool.start(worker)
        self.controller.threadpool.start(updater)

    def download(self):
        """Download the image set."""
        self.controller.dataset_controller.get_dataset()
        config.update_config_file(self.controller.config_file_name, 'dicom_folder', 'folder_path', self.controller.dataset_controller.folder_full_path)

    def update(self, progress_callback, finished_callback):
        """Updates the GUI's progress bar.

        Parameters
        ----------
        progress_callback : pyqtSignal(int)
            Used to emit a signal to the GUI to update the progress bar. Passed automatically by Updater class.
        finished_callback : pyqtSignal(int)
            Used to emit a signal to the GUI to update the text. Passed automatically by Updater class.
        """
        # Wait for the file to start downloading before updating progress bar
        while not os.path.exists(self.controller.dataset_controller.filename_fullpath):
            pass

        # Update the progress bar with the current file size
        progress_callback.emit(0)
        self.controller.log_gui_state('debug')
        while self.get_tgz_size() < self.get_tgz_max():
            progress_callback.emit(self.get_tgz_size())
            self.controller.log_gui_state('debug')
            time.sleep(1)
        progress_callback.emit(self.get_tgz_size())

        # Update the text and move to the next stage
        finished_callback.emit('Image download complete')
        self.controller.log_gui_state('debug')
        logging.info('***END DOWNLOADING PHASE***')
        self.controller.main_app.stage2_ui()

    def get_tgz_size(self):
        """Calculates the size of the TGZ file for the purpose of setting the progress bar value."""
        if self.controller.dataset == 'full_set':
            # Dividing by 100 because the expected size of this TGZ is larger than QProgressBar accepts
            return int(os.path.getsize(self.controller.dataset_controller.filename_fullpath) / 100)
        elif self.controller.dataset == 'subset':
            return os.path.getsize(self.controller.dataset_controller.filename_fullpath)
        else:
            raise ValueError('Value must be one of the keys in SOURCE_URL')

    def get_tgz_max(self):
        """Calculates the size of the TGZ file max for the purpose of setting the progress bar max."""
        if self.controller.dataset == 'full_set':
            # Dividing by 100 because the expected size of this TGZ is larger than QProgressBar accepts
            return int(self.controller.dataset_controller.expected_size / 100)
        elif self.controller.dataset == 'subset':
            return self.controller.dataset_controller.expected_size
        else:
            raise ValueError('Value must be one of the keys in SOURCE_URL')

class UnpackButton(QPushButton):
    def __init__(self, text, window, controller):
        QPushButton.__init__(self, text, window)
        self.clicked.connect(self.unpack_dataset)
        self.controller = controller

    def unpack_dataset(self):
        """Delegate the unpacking and GUI updating to 2 new threads."""
        logging.info('***BEGIN UNPACKING PHASE***')
        # Set the progress region
        self.controller.main_app.msg_box.setText('Unpacking images')
        self.controller.main_app.pro_bar.setMinimum(0)
        self.controller.main_app.pro_bar.setMaximum(self.controller.dataset_controller.expected_num_files)

        # Create 2 workers: 1 to unpack and 1 to update the progress bar
        worker = Worker(self.unpack)
        updater = Updater(self.update_unpack)
        # Connect the updater signal to the progress bar
        updater.signals.progress.connect(self.controller.main_app.update_pro_bar)
        updater.signals.finished.connect(self.controller.main_app.update_text)
        # Start the threads
        self.controller.threadpool.start(worker)
        self.controller.threadpool.start(updater)

    def unpack(self):
        """Unpack the image set."""
        self.controller.dataset_controller.unpack()

    def update_unpack(self, progress_callback, finished_callback):
        """Updates the GUI's progress bar.

        Parameters
        ----------
        progress_callback : pyqtSignal(int)
            Used to emit a signal to the GUI to update the progress bar. Passed automatically by Updater class.
        finished_callback : pyqtSignal(int)
            Used to emit a signal to the GUI to update the text. Passed automatically by Updater class.
        """
        # Wait for the folder to be available before updating progress bar
        while not os.path.isdir(self.controller.dataset_controller.folder_full_path):
            logging.debug('waiting')
            time.sleep(1)
            pass

        # Update the progress bar with the current file count in the folder path
        progress_callback.emit(0)
        self.controller.log_gui_state('debug')
        while self.count_DCMs(self.controller.dataset_controller.folder_full_path) < self.controller.dataset_controller.expected_num_files:
            progress_callback.emit(self.count_DCMs(self.controller.dataset_controller.folder_full_path))
            self.controller.log_gui_state('debug')
            time.sleep(1)
        progress_callback.emit(self.count_DCMs(self.controller.dataset_controller.folder_full_path))
        logging.debug('Final count: ' + str(self.count_DCMs(self.controller.dataset_controller.folder_full_path)))

        # Update the text and move to the next stage
        finished_callback.emit('Images unpacked')
        self.controller.log_gui_state('debug')
        logging.info('***END UNPACKING PHASE***')
        self.controller.main_app.stage3_ui()

    def count_DCMs(self, full_folder_path):
        return sum([len(files) for r, d, files in os.walk(full_folder_path) if any(item.endswith('.dcm') for item in files)])

class StoreButton(QPushButton):
    def __init__(self, text, window, controller):
        QPushButton.__init__(self, text, window)
        self.clicked.connect(self.store_metadata)
        self.controller = controller

    def store_metadata(self):
        """Delegate the storing of metadata and GUI updating to 2 new threads."""
        logging.info('***BEGIN STORING PHASE***')
        # Set the progress region
        self.controller.main_app.msg_box.setText('Storing metadata')
        self.controller.main_app.pro_bar.setMinimum(0)
        self.controller.main_app.pro_bar.setMaximum(self.controller.dataset_controller.expected_num_files)

        # Create 2 workers: 1 to store and 1 to update the progress bar
        worker = Worker(self.to_db, self.controller.dataset_controller.columns_info_full_path, self.controller.config_file_name, 'elements')
        updater = Updater(self.update_store)
        # Connect the updater signal to the progress bar
        updater.signals.progress.connect(self.controller.main_app.update_pro_bar)
        updater.signals.finished.connect(self.controller.main_app.update_text)
        # Start the threads
        self.controller.threadpool.start(worker)
        self.controller.threadpool.start(updater)

    def to_db(self, columns_info, config_file_name, section_name):
        """Store the metadata from the folder to Postgres.
        
        Parameters
        ----------
        columns_info : string
            The name of the JSON containing the column info of the DB table
        config_file_name : string
            The name of the INI config file containing DB info and folder locations
        section_name : string
            The name corresponding to the section of the columns_info to use
        """
        dicom_to_db(columns_info, config_file_name, section_name)

    def update_store(self, progress_callback, finished_callback):
        """Updates the GUI's progress bar.

        Parameters
        ----------
        progress_callback : pyqtSignal(int)
            Used to emit a signal to the GUI to update the progress bar. Passed automatically by Updater class.
        finished_callback : pyqtSignal(int)
            Used to emit a signal to the GUI to update the text. Passed automatically by Updater class.
        """
        # Wait for the table to be available before updating progress bar
        while not bdo.table_exists(self.controller.config_file_name, self.controller.db_name, self.controller.meta_table_name):
            pass
            
        # Update the progress bar with the current record count in the DB table
        progress_callback.emit(0)
        self.controller.log_gui_state('debug')
        while bdo.count_records(self.controller.config_file_name, self.controller.db_name, self.controller.meta_table_name) < self.controller.dataset_controller.expected_num_files:
            progress_callback.emit(bdo.count_records(self.controller.config_file_name, self.controller.db_name, self.controller.meta_table_name))
            self.controller.log_gui_state('debug')
            time.sleep(1)
        progress_callback.emit(bdo.count_records(self.controller.config_file_name, self.controller.db_name, self.controller.meta_table_name))
        
        # Update the text and move to the next stage
        finished_callback.emit('Done storing metadata')
        self.controller.log_gui_state('debug')
        logging.info('***END STORING PHASE***')
        self.controller.main_app.stage4_ui()

class CalculateButton(QPushButton):
    def __init__(self, text, window, controller):
        QPushButton.__init__(self, text, window)
        self.clicked.connect(self.calculate_features)
        self.controller = controller

    def calculate_features(self):
        """Delegate the feature calculating and GUI updating to 2 new threads."""
        logging.info('***BEGIN FEATURE CALCULATION PHASE***')
        # Set the progress region
        self.controller.main_app.msg_box.setText('Calculating features')
        self.controller.main_app.pro_bar.setMinimum(0)
        self.controller.main_app.pro_bar.setMaximum(self.controller.dataset_controller.expected_num_files)

        # Add table to DB
        bdo.add_table_to_db(self.controller.feat_table_name, self.controller.dataset_controller.columns_info_full_path, self.controller.config_file_name, 'features_list')

        # Create 2 workers: 1 to calculate features and 1 to update the progress bar
        worker = Worker(self.calc_feat, self.controller.config_file_name)
        updater = Updater(self.update_calc)
        # Connect the updater signal to the progress bar
        updater.signals.progress.connect(self.controller.main_app.update_pro_bar)
        updater.signals.finished.connect(self.controller.main_app.update_text)
        # Start the threads
        self.controller.threadpool.start(worker)
        self.controller.threadpool.start(updater)

    def calc_feat(self, config_file_name):
        """Calculate the features.
        
        Parameters
        ----------
        config_file_name : string
            The name of the INI config file containing DB info and folder locations
        """
        calculate_features(config_file_name)

    def update_calc(self, progress_callback, finished_callback):
        """Updates the GUI's progress bar.

        Parameters
        ----------
        progress_callback : pyqtSignal(int)
            Used to emit a signal to the GUI to update the progress bar. Passed automatically by Updater class.
        finished_callback : pyqtSignal(int)
            Used to emit a signal to the GUI to update the text. Passed automatically by Updater class.
        """
        # Wait for the table to be available before updating progress bar
        while not bdo.table_exists(self.controller.config_file_name, self.controller.db_name, self.controller.feat_table_name):
            pass
        
        # Update the progress bar with the current record count in the DB table
        progress_callback.emit(0)
        while bdo.count_records(self.controller.config_file_name, self.controller.db_name, self.controller.feat_table_name) < self.controller.dataset_controller.expected_num_files:
            progress_callback.emit(bdo.count_records(self.controller.config_file_name, self.controller.db_name, self.controller.feat_table_name))
            time.sleep(1)
        progress_callback.emit(bdo.count_records(self.controller.config_file_name, self.controller.db_name, self.controller.feat_table_name))

        # Update the text and move to the next stage
        finished_callback.emit('Done calculating features')
        logging.info('***END FEATURE CALCULATION PHASE***')
        self.controller.main_app.stage5_ui()
        
class LabelButton(QPushButton):
    def __init__(self, text, window, controller):
        QPushButton.__init__(self, text, window)
        self.clicked.connect(self.label_images)
        self.controller = controller

    def label_images(self):
        """Use an app to manually label images."""
        logging.info('***BEGIN LABELING PHASE***')
        # Set the progress region
        self.controller.main_app.pro_bar.setMinimum(0)
        self.controller.main_app.pro_bar.setMaximum(self.controller.dataset_controller.expected_num_files)
        if self.controller.dataset == 'subset':
            # Set the progress region
            self.controller.main_app.msg_box.setText('Please manually label images')
            
            # Add table to DB
            bdo.add_table_to_db(self.controller.label_table_name, self.controller.dataset_controller.columns_info_full_path, self.controller.config_file_name, 'labels')

            # Create 1 thread to update the progress bar as the app runs
            updater = Updater(self.check_done)
            # Connect the updater signal to the progress bar
            updater.signals.progress.connect(self.controller.main_app.update_pro_bar)
            updater.signals.finished.connect(self.controller.main_app.update_text)
            # Start the thread
            self.controller.threadpool.start(updater)

            # Open new window with the labeling app
            self.controller.label_app = LabelImageApplication(self.controller.config_file_name)
        elif self.controller.dataset == 'full_set':
            bdo.import_image_label_data(self.controller.label_table_name, self.controller.dataset_controller.parent_folder + '/' + 'image_labels.csv', self.controller.dataset_controller.columns_info_full_path, self.controller.config_file_name, 'labels')
            logging.info('***END LABELING PHASE***')
            self.controller.main_app.update_text('Done importing labels')
            self.controller.main_app.update_pro_bar(self.controller.dataset_controller.expected_num_files)
            self.controller.main_app.stage6_ui()
        else:
            raise ValueError('Value must be one of the keys in SOURCE_URL')
        
    def check_done(self, progress_callback, finished_callback):
        """Updates the GUI's progress bar."""
        # Continually check for the number of records in the DB table
        progress_callback.emit(0)
        while bdo.count_records(self.controller.config_file_name, self.controller.db_name, self.controller.label_table_name) < self.controller.dataset_controller.expected_num_files:
            progress_callback.emit(bdo.count_records(self.controller.config_file_name, self.controller.db_name, self.controller.label_table_name))
            time.sleep(1)
        progress_callback.emit(bdo.count_records(self.controller.config_file_name, self.controller.db_name, self.controller.label_table_name))

        # Update the text and move to the next stage
        finished_callback.emit('Done labeling')
        logging.info('***END LABELING PHASE***')
        self.controller.main_app.stage6_ui()

class ClassificationButton(QPushButton):
    def __init__(self, text, window, controller):
        QPushButton.__init__(self, text, window)
        self.clicked.connect(self.classification)
        self.controller = controller

    def classification(self):
        """Performs the training of classifier and gets the accuracy of the classifier."""
        logging.info('***BEGIN CLASSIFICATION PHASE***')
        self.controller.classifier, accuracy = classification(self.controller.config_file_name)
        self.controller.main_app.update_text('Accuracy: ' + str(accuracy))
        logging.info('***END CLASSIFICATION PHASE***')
