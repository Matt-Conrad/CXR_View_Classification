from stage import Stage, Runnable
import os
import logging
import requests
from PyQt5.QtCore import pyqtSlot
from ctypes import cdll

class DownloadStage(Stage):
    """Downloads datasets from online sources."""
    def __init__(self, configHandler):
        Stage.__init__(self)
        self.downloader = self.Downloader(configHandler)
        self.downloadUpdater = self.DownloadUpdater(configHandler)

    @pyqtSlot()
    def download(self):
        self.threadpool.start(self.downloader)
        self.threadpool.start(self.downloadUpdater)

    class Downloader(Runnable):
        def __init__(self, configHandler):
            Runnable.__init__(self, configHandler)

            self.lib = cdll.LoadLibrary(os.path.join(configHandler.getParentFolder(), "src", "libdownloader.so"))
            
            self.obj = self.lib.Downloader_new()

        def run(self): 
            self.lib.Downloader_run(self.obj)

    class DownloadUpdater(Runnable):
        """Controls logic of getting the dataset from online sources."""
        def __init__(self, configHandler):
            Runnable.__init__(self, configHandler)
            self.filenameAbsPath = configHandler.getTgzFilePath()
            self.datasetType = configHandler.getDatasetType()

        @pyqtSlot()
        def run(self):
            self.signals.attemptUpdateText.emit("Downloading images")
            self.signals.attemptUpdateProBarBounds.emit(0, self.getTgzMax())
            self.signals.attemptUpdateProBarValue.emit(0)

            while not os.path.isfile(self.filenameAbsPath):
                pass
            
            while self.getTgzSize() < self.expectedSize:
                self.signals.attemptUpdateProBarValue.emit(self.getTgzSize())

            self.signals.attemptUpdateProBarValue.emit(self.getTgzSize())
            self.signals.attemptUpdateText.emit("Image download complete")
            self.signals.finished.emit()

        def getTgzSize(self):
            """Calculates the size of the TGZ file."""
            if self.datasetType == 'full_set':
                # Dividing by 100 because the expected size of this TGZ is larger than QProgressBar accepts
                return int(os.path.getsize(self.filenameAbsPath) / 100)
            elif self.datasetType == 'subset':
                return os.path.getsize(self.filenameAbsPath)
            else:
                raise ValueError('Value must be one of the keys in SOURCE_URL')

        def getTgzMax(self):
            """Calculates the size of the TGZ file max."""
            if self.datasetType == 'full_set':
                # Dividing by 100 because the expected size of this TGZ is larger than QProgressBar accepts
                return int(self.expectedSize / 100)
            elif self.datasetType== 'subset':
                return self.expectedSize
            else:
                raise ValueError('Value must be one of the keys in SOURCE_URL')
