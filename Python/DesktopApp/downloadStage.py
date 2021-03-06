from stage import Stage, Runnable
import os
import logging
import requests
from PyQt5.QtCore import pyqtSlot

import time

class DownloadStage(Stage):
    """Downloads datasets from online sources."""
    def __init__(self, configHandler):
        Stage.__init__(self)
        self.downloader = self.Downloader(configHandler)

    @pyqtSlot()
    def download(self):
        self.threadpool.start(self.downloader)

    class Downloader(Runnable):
        def __init__(self, configHandler):
            Runnable.__init__(self, configHandler)
            self.tgzFilePath = configHandler.getTgzFilePath()
            self.datasetType = configHandler.getDatasetType()

        @pyqtSlot()
        def run(self):
            start = time.time()
            logging.info('Checking if %s already exists', self.tgzFilePath)
            if os.path.isfile(self.tgzFilePath):
                logging.info('%s already exists', self.tgzFilePath)
                logging.info('Checking if %s was downloaded properly', self.tgzFilePath)
                
                if os.path.getsize(self.tgzFilePath) == self.expectedSize:
                    logging.info('%s was downloaded properly', self.tgzFilePath)
                    end = time.time()
                    print(end - start)
                    self.signals.attemptUpdateProBarValue.emit(self.getTgzSize())
                    self.signals.attemptUpdateText.emit("Image download complete")
                    self.signals.finished.emit()
                else:
                    logging.warning('%s was NOT downloaded properly', self.tgzFilePath)
                    logging.info('Removing %s', self.tgzFilePath)
                    os.remove(self.tgzFilePath)
                    logging.info('Successfully removed %s', self.tgzFilePath)
                    self.downloadDataset()
            else:
                logging.info('%s does not exist', self.tgzFilePath)
                self.downloadDataset()
            

        def downloadDataset(self):
            logging.info('Downloading dataset from %s', self.configHandler.getUrl())

            self.signals.attemptUpdateText.emit("Downloading images")
            self.signals.attemptUpdateProBarBounds.emit(0, self.getTgzMax())
            self.signals.attemptUpdateProBarValue.emit(0)

            with requests.get(self.configHandler.getUrl(), stream=True) as r:
                r.raise_for_status() # Raise error if something goes wrong with connection
                with open(self.tgzFilePath, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk: # filter out keep-alive new chunks
                            self.signals.attemptUpdateProBarValue.emit(self.getTgzSize())
                            f.write(chunk)
                        
            self.run() #######

        def getTgzSize(self):
            """Calculates the size of the TGZ file."""
            try:
                preAdjustedSize = os.path.getsize(self.tgzFilePath)
            except FileNotFoundError:
                return None

            if self.datasetType == 'full_set':
                # Dividing by 100 because the expected size of this TGZ is larger than QProgressBar accepts
                return int(preAdjustedSize / 100)
            elif self.datasetType == 'subset':
                return preAdjustedSize

        def getTgzMax(self):
            """Calculates the size of the TGZ file max."""
            if self.datasetType == 'full_set':
                # Dividing by 100 because the expected size of this TGZ is larger than QProgressBar accepts
                return int(self.expectedSize / 100)
            elif self.datasetType== 'subset':
                return self.expectedSize