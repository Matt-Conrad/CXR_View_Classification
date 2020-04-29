"""Provides the functionality of the calculate button."""
import time
import logging
from calculate_features import calculate_features
import DicomToDatabase.basic_db_ops as bdo
from workers import Worker, Updater

class calculate_functionality():
    def __init__(self, controller):
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