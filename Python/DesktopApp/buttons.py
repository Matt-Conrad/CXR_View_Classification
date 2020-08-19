"""Contains the code for the buttons for the app GUI."""
import logging
import os
import time
from PyQt5.QtWidgets import QPushButton
from classification import classification
from workers import Worker, Updater
import metadata_to_db.basic_db_ops as bdo
import metadata_to_db.config as config
from metadata_to_db.dicom_to_db import dicom_to_db
from LabelImages import LabelImageApplication
        
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
            updater.signals.progress.connect(self.controller.main_app.update_pro_bar_val)
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
