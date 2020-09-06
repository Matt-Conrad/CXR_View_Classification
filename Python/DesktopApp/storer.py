from PyQt5.QtCore import pyqtSlot, pyqtSignal
from stage import Stage
from metadata_to_db.dicom_to_db import DicomToDatabase

class Storer(Stage):
    """Class for moving all DCM tag-values from a directory of DCMs into a PostgreSQL DB."""
    startUpdating = pyqtSignal()

    def __init__(self, configHandler, dbHandler):
        Stage.__init__(self, configHandler, dbHandler)
        self.dicomToDatabase = DicomToDatabase(configHandler, dbHandler)

    @pyqtSlot()
    def run(self):
        metaTableName = self.configHandler.getTableName("metadata")
        columnsInfoPath = self.configHandler.getColumnsInfoPath()

        if not self.dbHandler.table_exists(metaTableName):
            self.dbHandler.add_table_to_db(metaTableName, columnsInfoPath, "elements")
        self.startUpdating.emit()

        self.dicomToDatabase.dicomToDb(self.dbHandler.dbInfo['database'], metaTableName, columnsInfoPath)

class StoreUpdater(Stage):
    """Updates dashboard for the storer class."""
    def __init__(self, configHandler, dbHandler):
        Stage.__init__(self, configHandler, dbHandler)
        self.folderRelPath = "./" + configHandler.getDatasetName()

    @pyqtSlot()
    def update(self):
        self.attemptUpdateText.emit("Storing metadata")
        self.attemptUpdateProBarBounds.emit(0, self.expected_num_files)
        self.attemptUpdateProBarValue.emit(0)

        while not self.dbHandler.table_exists(self.configHandler.getTableName('metadata')):
            pass

        while self.dbHandler.count_records(self.configHandler.getTableName('metadata')) != self.expected_num_files:
            self.attemptUpdateProBarValue.emit(self.dbHandler.count_records(self.configHandler.getTableName('metadata')))
            
        self.attemptUpdateProBarValue.emit(self.dbHandler.count_records(self.configHandler.getTableName('metadata')))
        self.finished.emit()
        self.attemptUpdateText.emit("Done storing metadata")