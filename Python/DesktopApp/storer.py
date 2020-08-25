"""Contains script that moves all DCM tag-values from a directory of DCMs into a PostgreSQL DB."""
from PyQt5.QtCore import pyqtSlot
from stage import Stage
from metadata_to_db.dicom_to_db import DicomToDatabase

class Storer(Stage):
    """Controls logic of getting the dataset from online sources."""
    def __init__(self, configHandler, dbHandler):
        Stage.__init__(self, configHandler, dbHandler)
        self.dicomToDatabase = DicomToDatabase(configHandler, dbHandler)

    @pyqtSlot()
    def store(self):
        self.dicomToDatabase.dicomToDb()

class StoreUpdater(Stage):
    """Controls logic of getting the dataset from online sources."""
    def __init__(self, configHandler, dbHandler):
        Stage.__init__(self, configHandler, dbHandler)
        self.folderRelPath = "./" + configHandler.getDatasetName()

    @pyqtSlot()
    def update(self):
        self.attemptUpdateText.emit("Storing metadata")
        self.attemptUpdateProBarBounds.emit(0, self.expected_num_files)
        self.attemptUpdateProBarValue.emit(0)
        
        while self.dbHandler.count_records(self.configHandler.getTableName('metadata')) != self.expected_num_files:
            self.attemptUpdateProBarValue.emit(self.dbHandler.count_records(self.configHandler.getTableName('metadata')))
            
        self.attemptUpdateProBarValue.emit(self.dbHandler.count_records(self.configHandler.getTableName('metadata')))
        self.attemptUpdateText.emit("Done storing metadata")
        self.finished.emit()