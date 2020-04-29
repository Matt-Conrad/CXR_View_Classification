"""Provides the functionality of the classification button."""
import logging
from classification import classification

class classification_functionality():
    def __init__(self, controller):
        self.controller = controller

    def classification(self):
        """Performs the training of classifier and gets the accuracy of the classifier."""
        logging.info('***BEGIN CLASSIFICATION PHASE***')
        self.controller.classifier, accuracy = classification(self.controller.config_file_name)
        self.controller.main_app.update_text('Accuracy: ' + str(accuracy))
        logging.info('***END CLASSIFICATION PHASE***')