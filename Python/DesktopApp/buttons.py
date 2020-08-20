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
