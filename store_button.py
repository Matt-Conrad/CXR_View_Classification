"""Provides the functionality of the store button."""
import time
import logging
import DicomToDatabase.basic_db_ops as bdo
from DicomToDatabase.dicom_to_db import dicom_to_db
from workers import Worker, Updater

class store_functionality():
    def __init__(self, controller):
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