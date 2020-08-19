from stage import Stage
import os
import logging
import requests
from PyQt5.QtCore import pyqtSlot, pyqtSignal

class Downloader(Stage):
    """Controls logic of getting the dataset from online sources."""

    def __init__(self, configHandler):
        Stage.__init__(self, configHandler)
        self.filenameRelPath = "./" + configHandler.getTgzFilename()
        self.datasetType = configHandler.getDatasetType()

    @pyqtSlot()
    def get_dataset(self):
        """Attempt to get the dataset TGZ as many times as it takes. This one gets called by main.py"""
        logging.info('Checking if %s already exists', self.filenameRelPath)
        if os.path.isfile(self.filenameRelPath):
            logging.info('%s already exists', self.filenameRelPath)
            logging.info('Checking if %s was downloaded properly', self.filenameRelPath)
            
            if os.path.getsize(self.filenameRelPath) == self.expected_size:
                logging.info('%s was downloaded properly', self.filenameRelPath)
            else:
                logging.warning('%s was NOT downloaded properly', self.filenameRelPath)
                logging.info('Removing %s', self.filenameRelPath)
                os.remove(self.filenameRelPath)
                logging.info('Successfully removed %s', self.filenameRelPath)
                self.download()
        else:
            logging.info('%s does not exist', self.filenameRelPath)
            self.download()

        self.attemptUpdateProBarValue.emit(self.getTgzSize())
        self.attemptUpdateText.emit("Image download complete")
        self.finished.emit()

    def download(self):
        """Download the dataset, invoke the checks in get_dataset after.
        
        This runs after get_dataset figures out the current state of the downloading.
        """
        # Start download
        logging.info('Downloading dataset from %s', self.configHandler.getUrl())

        self.attemptUpdateText.emit("Downloading images")
        self.attemptUpdateProBarBounds.emit(0, self.getTgzMax())
        self.attemptUpdateProBarValue.emit(0)

        with requests.get(self.configHandler.getUrl(), stream=True) as r:
            r.raise_for_status() # Raise error if something goes wrong with connection
            with open(self.filenameRelPath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk: # filter out keep-alive new chunks
                        self.attemptUpdateProBarValue.emit(self.getTgzSize())
                        f.write(chunk)
                    
        self.get_dataset()

    def getTgzSize(self):
        """Calculates the size of the TGZ file for the purpose of setting the progress bar value."""
        if self.datasetType == 'full_set':
            # Dividing by 100 because the expected size of this TGZ is larger than QProgressBar accepts
            return int(os.path.getsize(self.filenameRelPath) / 100)
        elif self.datasetType == 'subset':
            return os.path.getsize(self.filenameRelPath)
        else:
            raise ValueError('Value must be one of the keys in SOURCE_URL')

    def getTgzMax(self):
        """Calculates the size of the TGZ file max for the purpose of setting the progress bar max."""
        if self.datasetType == 'full_set':
            # Dividing by 100 because the expected size of this TGZ is larger than QProgressBar accepts
            return int(self.expected_size / 100)
        elif self.datasetType== 'subset':
            return self.expected_size
        else:
            raise ValueError('Value must be one of the keys in SOURCE_URL')