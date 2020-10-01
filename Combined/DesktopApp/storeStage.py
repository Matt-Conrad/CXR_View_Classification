from stage import Stage, Runnable
from PyQt5.QtCore import pyqtSlot
from metadata_to_db.dicomToDb import DicomToDatabase

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
            self.dicomToDatabase = DicomToDatabase(configHandler, dbHandler)

        @pyqtSlot()
        def run(self):
            metaTableName = self.configHandler.getTableName("metadata")
            columnsInfoPath = self.configHandler.getColumnsInfoPath()

            if not self.dbHandler.tableExists(metaTableName):
                self.dbHandler.addTableToDb(metaTableName, columnsInfoPath, "nonElementColumns", "elements")

            self.dicomToDatabase.dicomToDb(self.dbHandler.dbInfo['database'], metaTableName, columnsInfoPath)

    class StoreUpdater(Runnable):
        def __init__(self, configHandler, dbHandler):
            Runnable.__init__(self, configHandler, dbHandler)
            self.folderRelPath = "./" + configHandler.getDatasetName()

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