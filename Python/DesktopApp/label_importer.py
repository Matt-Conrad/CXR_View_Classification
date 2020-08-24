from stage import Stage
from PyQt5.QtCore import pyqtSlot

class LabelImporter(Stage):
    """Contains code for the application used to assist in labeling the data."""

    def __init__(self, configHandler, dbHandler):
        """"""
        Stage.__init__(self, configHandler, dbHandler)
    
    @pyqtSlot()
    def importLabels(self):
        self.attemptUpdateProBarBounds.emit(0,1)
        self.attemptUpdateProBarValue.emit(0)
        self.attemptUpdateText.emit("Importing label data")
        self.dbHandler.add_table_to_db(self.configHandler.getTableName('label'), self.configHandler.getColumnsInfoPath(), 'labels')
        self.dbHandler.import_image_label_data()
        self.attemptUpdateProBarValue.emit(1)
        self.attemptUpdateText.emit("Done importing")
        self.finished.emit()
        