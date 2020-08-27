from stage import Stage
import json
import logging
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
        self.import_image_label_data()
        
        self.attemptUpdateProBarValue.emit(1)
        self.attemptUpdateText.emit("Done importing")
        self.finished.emit()

    def import_image_label_data(self):
        logging.info('Attempting to import CSV into table in DB')

        with open(self.configHandler.getColumnsInfoPath()) as file_reader:
            elements_json = json.load(file_reader)
        elements = elements_json['labels']

        sql_query = 'COPY ' + self.configHandler.getTableName('label') + '(file_name, file_path, '
        for element_name in elements:
            if not elements[element_name]['calculation_only']:
                sql_query = sql_query + element_name + ','
        sql_query = sql_query[:-1] + ') FROM \'' + self.configHandler.getParentFolder() + "/" + self.configHandler.getCsvPath() + '\' DELIMITER \',\' CSV HEADER;'

        self.dbHandler.executeQuery(self.dbHandler.storeCursor, sql_query)
        self.dbHandler.count_records(self.configHandler.getTableName('label'))
        