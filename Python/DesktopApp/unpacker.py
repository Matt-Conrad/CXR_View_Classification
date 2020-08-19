from stage import Stage
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QThread, QObject
import tarfile
import logging
import os

class Unpacker(Stage):
    """Controls logic of getting the dataset from online sources."""
    def __init__(self, configHandler):
        Stage.__init__(self, configHandler)
        self.folderRelPath = "./" + configHandler.getDatasetName()

    @pyqtSlot()
    def unpack(self):
        """Unpack the dataset from the TGZ and put it in a folder."""
        filenameRelPath = "./" + self.configHandler.getTgzFilename()

        logging.info('Unpacking dataset from %s', filenameRelPath)

        tf = tarfile.open(filenameRelPath)
        tf.extractall(path=self.folderRelPath)
        
        self.finished.emit()

        logging.info('Done unpacking')

    
class UnpackUpdater(QObject):
    """Controls logic of getting the dataset from online sources."""
    attemptUpdateProBarValue = pyqtSignal(int)
    attemptUpdateText = pyqtSignal(str)
    attemptUpdateProBarBounds = pyqtSignal(int, int)
    finished = pyqtSignal()

    def __init__(self, configHandler, expected_num_files):
        QObject.__init__(self)
        self.folderRelPath = "./" + configHandler.getDatasetName()
        self.expected_num_files = expected_num_files

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
