from stage import Stage, Runnable
from PyQt5.QtCore import pyqtSlot
from metadata_to_db.dicomToDb import DicomToDatabase
from ctypes import cdll
import os

import time

class StoreStage(Stage):
    def __init__(self, configHandler, dbHandler):
        Stage.__init__(self)
        self.storer = self.Storer(configHandler, dbHandler)
        self.storeUpdater = self.StoreUpdater(configHandler, dbHandler)

    @pyqtSlot()
    def store(self):
        self.threadpool.start(self.storer)
        self.threadpool.start(self.storeUpdater)

    class Storer(Runnable):
        def __init__(self, configHandler, dbHandler):
            Runnable.__init__(self, configHandler, dbHandler)

            self.lib = cdll.LoadLibrary(os.path.join(configHandler.getParentFolder(), "cmake_build", "libstorer.so"))
            
            self.obj = self.lib.Storer_new()

        @pyqtSlot()
        def run(self):
            start = time.time()
            self.lib.Storer_run(self.obj)
            end = time.time()
            print(end - start)

    class StoreUpdater(Runnable):
        def __init__(self, configHandler, dbHandler):
            Runnable.__init__(self, configHandler, dbHandler)

        @pyqtSlot()
        def run(self):
            self.signals.attemptUpdateText.emit("Storing metadata")
            self.signals.attemptUpdateProBarBounds.emit(0, self.expectedNumFiles)
            self.signals.attemptUpdateProBarValue.emit(0)

            while not self.dbHandler.tableExists(self.configHandler.getTableName('metadata')):
                pass

            while self.dbHandler.countRecords(self.configHandler.getTableName('metadata')) != self.expectedNumFiles:
                self.signals.attemptUpdateProBarValue.emit(self.dbHandler.countRecords(self.configHandler.getTableName('metadata')))
                
            self.signals.attemptUpdateProBarValue.emit(self.dbHandler.countRecords(self.configHandler.getTableName('metadata')))
            self.signals.finished.emit()
            self.signals.attemptUpdateText.emit("Done storing metadata")