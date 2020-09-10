from stage import Stage, Runnable
import json
import logging
from PyQt5.QtCore import pyqtSlot

class LabelImportStage(Stage):
    def __init__(self, configHandler, dbHandler):
        Stage.__init__(self, configHandler, dbHandler)
        self.labelImporter = self.LabelImporter(configHandler, dbHandler)

    @pyqtSlot()
    def importLabels(self):
        self.threadpool.start(self.labelImporter)

    class LabelImporter(Runnable):
        """Class for importing image labels from CSV."""
        def __init__(self, configHandler, dbHandler):
            Runnable.__init__(self, configHandler, dbHandler)
        
        @pyqtSlot()
        def run(self):
            logging.info("Importing label data from CSV")
            self.signals.attemptUpdateProBarBounds.emit(0,1)
            self.signals.attemptUpdateProBarValue.emit(0)
            self.signals.attemptUpdateText.emit("Importing label data")

            self.dbHandler.add_table_to_db(self.configHandler.getTableName('label'), self.configHandler.getColumnsInfoPath(), 'labels')
            self.import_image_label_data()
            
            self.signals.attemptUpdateProBarValue.emit(1)
            self.signals.attemptUpdateText.emit("Done importing")
            self.signals.finished.emit()
            logging.info("Done importing label data")

        def import_image_label_data(self):
            with open(self.configHandler.getColumnsInfoPath()) as file_reader:
                elements_json = json.load(file_reader)
            elements = elements_json['labels']

            sql_query = 'COPY ' + self.configHandler.getTableName('label') + '(file_name, file_path, '
            for element_name in elements:
                if not elements[element_name]['calculation_only']:
                    sql_query = sql_query + element_name + ','
            sql_query = sql_query[:-1] + ') FROM \'' + self.configHandler.getParentFolder() + "/" + self.configHandler.getCsvPath() + '\' DELIMITER \',\' CSV HEADER;'
            self.dbHandler.executeQuery(self.dbHandler.connection, sql_query)
            self.dbHandler.count_records(self.configHandler.getTableName('label'))
        