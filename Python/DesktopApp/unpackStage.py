from stage import Stage, Runnable
from PyQt5.QtCore import pyqtSlot
import tarfile
import logging
import os

import time

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

        @pyqtSlot()
        def run(self):
            start = time.time()
            tgzFilePath = self.configHandler.getTgzFilePath()

            logging.info('Unpacking dataset from %s', tgzFilePath)

            tf = tarfile.open(tgzFilePath)
            tf.extractall(path=self.configHandler.getUnpackFolderPath())

            logging.info('Done unpacking')
            # end = time.time()
            # print(end - start)

    class UnpackUpdater(Runnable):
        """Controls logic of getting the dataset from online sources."""
        def __init__(self, configHandler):
            Runnable.__init__(self, configHandler)

        @pyqtSlot()
        def run(self):
            self.signals.attemptUpdateText.emit("Unpacking Images")
            self.signals.attemptUpdateProBarBounds.emit(0, self.expectedNumFiles)
            self.signals.attemptUpdateProBarValue.emit(0)
            
            while self.countDcms() != self.expectedNumFiles:
                self.signals.attemptUpdateProBarValue.emit(self.countDcms())

            self.signals.attemptUpdateProBarValue.emit(self.countDcms())
            self.signals.attemptUpdateText.emit("Images unpacked")
            self.signals.finished.emit()

        def countDcms(self):
            return sum([len(files) for r, d, files in os.walk(self.configHandler.getUnpackFolderPath()) if any(item.endswith('.dcm') for item in files)])

