from stage import Stage, Runnable
from PyQt5.QtCore import pyqtSlot
import tarfile
import logging
import os
from ctypes import cdll, c_char_p

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
        def __init__(self, configHandler):
            Runnable.__init__(self, configHandler)

            self.lib = cdll.LoadLibrary(os.path.join(configHandler.getParentFolder(), "cmake_build", "libunpacker.so"))
            
            self.obj = self.lib.Unpacker_new()

        def run(self): 
            start = time.time()
            self.lib.Unpacker_run(self.obj)
            end = time.time()
            print(end - start)

    class UnpackUpdater(Runnable):
        """Controls logic of getting the dataset from online sources."""
        def __init__(self, configHandler):
            Runnable.__init__(self, configHandler)
            self.folderAbsPath = configHandler.getUnpackFolderPath()

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
            return sum([len(files) for r, d, files in os.walk(self.folderAbsPath) if any(item.endswith('.dcm') for item in files)])

