from stage import Stage
from PyQt5.QtCore import pyqtSlot
import tarfile
import logging
import os

class Unpacker(Stage):
    """Controls logic of getting the dataset from online sources."""
    def __init__(self, configHandler):
        Stage.__init__(self, configHandler)
        self.folderRelPath = "./" + configHandler.getDatasetName()

    @pyqtSlot()
    def run(self):
        filenameRelPath = "./" + self.configHandler.getTgzFilename()

        logging.info('Unpacking dataset from %s', filenameRelPath)

        tf = tarfile.open(filenameRelPath)
        tf.extractall(path=self.folderRelPath)

        logging.info('Done unpacking')

    
class UnpackUpdater(Stage):
    """Controls logic of getting the dataset from online sources."""
    def __init__(self, configHandler):
        Stage.__init__(self, configHandler)
        self.folderRelPath = "./" + configHandler.getDatasetName()

    @pyqtSlot()
    def update(self):
        self.attemptUpdateText.emit("Unpacking Images")
        self.attemptUpdateProBarBounds.emit(0, self.expected_num_files)
        self.attemptUpdateProBarValue.emit(0)
        
        while self.count_DCMs() != self.expected_num_files:
            self.attemptUpdateProBarValue.emit(self.count_DCMs())
            
        self.attemptUpdateProBarValue.emit(self.count_DCMs())
        self.attemptUpdateText.emit("Images unpacked")
        self.finished.emit()

    def count_DCMs(self):
        return sum([len(files) for r, d, files in os.walk(self.folderRelPath) if any(item.endswith('.dcm') for item in files)])
