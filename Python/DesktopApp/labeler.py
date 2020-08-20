"""Contains script that moves all DCM tag-values from a directory of DCMs into a PostgreSQL DB."""
from stage import Stage
from PyQt5.QtCore import pyqtSlot
from LabelImages import LabelImageApplication
import logging

class Labeler(Stage):
    """Controls logic of getting the dataset from online sources."""
    def __init__(self, configHandler, dbHandler):
        Stage.__init__(self, configHandler, dbHandler)

    @pyqtSlot()
    def label_images(self):
        """Use an app to manually label images."""
        logging.info('***BEGIN LABELING PHASE***')
        # Set the progress region
        self.attemptUpdateProBarBounds.emit(0, self.expected_num_files)
        if self.configHandler.getDatasetType() == 'subset':
            # Set the progress region
            self.attemptUpdateText.emit('Please manually label images')
            
            # Add table to DB
            self.dbHandler.add_table_to_db(self.configHandler.getTableName('label'), self.configHandler.getColumnsInfoPath(), 'labels')

            # Open new window with the labeling app
            self.label_app = LabelImageApplication(self.configHandler, self.dbHandler)
            self.label_app.finished.connect(self.finished)
            self.label_app.attemptUpdateProBarValue.connect(self.attemptUpdateProBarValue)
            self.label_app.attemptUpdateProBarBounds.connect(self.attemptUpdateProBarBounds)
            self.label_app.attemptUpdateText.connect(self.attemptUpdateText)
        elif self.configHandler.getDatasetType() == 'full_set':
            bdo.import_image_label_data(self.configHandler.getTableName('label'), self.configHandler.getCsvPath(), self.configHandler.getColumnsInfoPath(), self.configHandler.getConfigFilename(), 'labels')
            logging.info('***END LABELING PHASE***')
            self.attemptUpdateText.emit('Done importing labels')
            self.attemptUpdateProBarValue.emit(self.expected_num_files)
            self.finished.emit()
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