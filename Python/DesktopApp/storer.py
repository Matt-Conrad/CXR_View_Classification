"""Contains script that moves all DCM tag-values from a directory of DCMs into a PostgreSQL DB."""
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from stage import Stage
from metadata_to_db.dicom_to_db import DicomToDatabase

class Storer(Stage):
    """Controls logic of getting the dataset from online sources."""
    def __init__(self, configHandler, dbHandler):
        Stage.__init__(self, configHandler, dbHandler)
        self.dicomToDatabase = DicomToDatabase(configHandler, dbHandler, self.expected_num_files)

        self.dicomToDatabase.finished.connect(self.finished)
        self.dicomToDatabase.attemptUpdateProBarValue.connect(self.attemptUpdateProBarValue)
        self.dicomToDatabase.attemptUpdateProBarBounds.connect(self.attemptUpdateProBarBounds)
        self.dicomToDatabase.attemptUpdateText.connect(self.attemptUpdateText)

    @pyqtSlot()
    def dicomToDb(self):
        self.dicomToDatabase.dicomToDb()