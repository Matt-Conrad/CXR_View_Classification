from stage import Stage, Runnable
from PyQt5.QtCore import pyqtSlot, QThreadPool, QObject
from metadata_to_db.dicom_to_db import DicomToDatabase

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

            if not self.dbHandler.table_exists(metaTableName):
                self.dbHandler.add_table_to_db(metaTableName, columnsInfoPath, "elements")

            self.dicomToDatabase.dicomToDb(self.dbHandler.dbInfo['database'], metaTableName, columnsInfoPath)

    class StoreUpdater(Runnable):
        def __init__(self, configHandler, dbHandler):
            Runnable.__init__(self, configHandler, dbHandler)
            self.folderRelPath = "./" + configHandler.getDatasetName()

        @pyqtSlot()
        def run(self):
            self.signals.attemptUpdateText.emit("Storing metadata")
            self.signals.attemptUpdateProBarBounds.emit(0, self.expected_num_files)
            self.signals.attemptUpdateProBarValue.emit(0)

            while not self.dbHandler.table_exists(self.configHandler.getTableName('metadata')):
                pass

            while self.dbHandler.count_records(self.configHandler.getTableName('metadata')) != self.expected_num_files:
                self.signals.attemptUpdateProBarValue.emit(self.dbHandler.count_records(self.configHandler.getTableName('metadata')))
                
            self.signals.attemptUpdateProBarValue.emit(self.dbHandler.count_records(self.configHandler.getTableName('metadata')))
            self.signals.finished.emit()
            self.signals.attemptUpdateText.emit("Done storing metadata")