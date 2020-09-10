from stage import Stage, Runnable
import os
import logging
import requests
from PyQt5.QtCore import pyqtSlot

class DownloadStage(Stage):
    """Downloads datasets from online sources."""
    def __init__(self, configHandler):
        Stage.__init__(self, configHandler)
        self.downloader = self.Downloader(configHandler)

    @pyqtSlot()
    def download(self):
        self.threadpool.start(self.downloader)

    class Downloader(Runnable):
        def __init__(self, configHandler):
            Runnable.__init__(self, configHandler)
            self.filenameRelPath = "./" + configHandler.getTgzFilename()
            self.datasetType = configHandler.getDatasetType()

        @pyqtSlot()
        def run(self):
            logging.info('Checking if %s already exists', self.filenameRelPath)
            if os.path.isfile(self.filenameRelPath):
                logging.info('%s already exists', self.filenameRelPath)
                logging.info('Checking if %s was downloaded properly', self.filenameRelPath)
                
                if os.path.getsize(self.filenameRelPath) == self.expected_size:
                    logging.info('%s was downloaded properly', self.filenameRelPath)
                    self.signals.attemptUpdateProBarValue.emit(self.getTgzSize())
                    self.signals.attemptUpdateText.emit("Image download complete")
                    self.signals.finished.emit()
                else:
                    logging.warning('%s was NOT downloaded properly', self.filenameRelPath)
                    logging.info('Removing %s', self.filenameRelPath)
                    os.remove(self.filenameRelPath)
                    logging.info('Successfully removed %s', self.filenameRelPath)
                    self.downloadDataset()
            else:
                logging.info('%s does not exist', self.filenameRelPath)
                self.downloadDataset()

        def downloadDataset(self):
            logging.info('Downloading dataset from %s', self.configHandler.getUrl())

            self.signals.attemptUpdateText.emit("Downloading images")
            self.signals.attemptUpdateProBarBounds.emit(0, self.getTgzMax())
            self.signals.attemptUpdateProBarValue.emit(0)

            with requests.get(self.configHandler.getUrl(), stream=True) as r:
                r.raise_for_status() # Raise error if something goes wrong with connection
                with open(self.filenameRelPath, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk: # filter out keep-alive new chunks
                            self.signals.attemptUpdateProBarValue.emit(self.getTgzSize())
                            f.write(chunk)
                        
            self.run() #######

        def getTgzSize(self):
            """Calculates the size of the TGZ file."""
            if self.datasetType == 'full_set':
                # Dividing by 100 because the expected size of this TGZ is larger than QProgressBar accepts
                return int(os.path.getsize(self.filenameRelPath) / 100)
            elif self.datasetType == 'subset':
                return os.path.getsize(self.filenameRelPath)
            else:
                raise ValueError('Value must be one of the keys in SOURCE_URL')

        def getTgzMax(self):
            """Calculates the size of the TGZ file max."""
            if self.datasetType == 'full_set':
                # Dividing by 100 because the expected size of this TGZ is larger than QProgressBar accepts
                return int(self.expected_size / 100)
            elif self.datasetType== 'subset':
                return self.expected_size
            else:
                raise ValueError('Value must be one of the keys in SOURCE_URL')