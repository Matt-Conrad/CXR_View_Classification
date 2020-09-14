from stage import Stage, Runnable
from PyQt5.QtCore import pyqtSlot
import tarfile
import logging
import os

class UnpackStage(Stage):
    def __init__(self, configHandler):
        Stage.__init__(self)
        self.unpacker = self.Unpacker(configHandler)
        self.unpackUpdater = self.UnpackUpdater(configHandler)

    @pyqtSlot()
    def unpack(self):
        self.threadpool.start(self.unpacker)
        self.threadpool.start(self.unpackUpdater)

    class Unpacker(Runnable):
        """Controls logic of getting the dataset from online sources."""
        def __init__(self, configHandler):
            Runnable.__init__(self, configHandler)
            self.folderRelPath = "./" + configHandler.getDatasetName()

        @pyqtSlot()
        def run(self):
            filenameRelPath = "./" + self.configHandler.getTgzFilename()

            logging.info('Unpacking dataset from %s', filenameRelPath)

            tf = tarfile.open(filenameRelPath)
            tf.extractall(path=self.folderRelPath)

            logging.info('Done unpacking')

    class UnpackUpdater(Runnable):
        """Controls logic of getting the dataset from online sources."""
        def __init__(self, configHandler):
            Runnable.__init__(self, configHandler)
            self.folderRelPath = "./" + configHandler.getDatasetName()

        @pyqtSlot()
        def run(self):
            self.signals.attemptUpdateText.emit("Unpacking Images")
            self.signals.attemptUpdateProBarBounds.emit(0, self.expected_num_files)
            self.signals.attemptUpdateProBarValue.emit(0)
            
            while self.count_DCMs() != self.expected_num_files:
                self.signals.attemptUpdateProBarValue.emit(self.count_DCMs())
                
            self.signals.attemptUpdateProBarValue.emit(self.count_DCMs())
            self.signals.attemptUpdateText.emit("Images unpacked")
            self.signals.finished.emit()

        def count_DCMs(self):
            return sum([len(files) for r, d, files in os.walk(self.folderRelPath) if any(item.endswith('.dcm') for item in files)])

