import logging
import os
import psycopg2
import json
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from stage import Stage, Runnable

class LabelStage(Stage):
    """Downloads datasets from online sources."""
    def __init__(self, configHandler, dbHandler):
        Stage.__init__(self)
        if configHandler.getDatasetType() == "subset":
            self.labeler = self.ManualLabeler(configHandler, dbHandler)
        elif configHandler.getDatasetType() == "full_set":
            self.labeler = self.LabelImporter(configHandler, dbHandler)
        else:
            raise ValueError('Value must be one of the keys in SOURCE_URL')

    @pyqtSlot()
    def label(self):
        self.threadpool.start(self.labeler)

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

    class ManualLabeler(Runnable):
        """Class used to assist in labeling the data."""
        def __init__(self, configHandler, dbHandler):
            Runnable.__init__(self, configHandler, dbHandler)

            self.count = 0
            self.records = None
            self.record = None

        @pyqtSlot()
        def run(self):
            """Displays the content into the window."""
            logging.debug('Filling window')
            self.query_image_list()
            
            self.signals.attemptUpdateText.emit("Please manually label images")
            self.signals.attemptUpdateProBarBounds.emit(0, self.expected_num_files)

            self.dbHandler.add_table_to_db(self.configHandler.getTableName('label'), self.configHandler.getColumnsInfoPath(), 'labels')
            
            self.display_next_image()

            while self.count < self.expected_num_files:
                pass

            logging.info('End of query')
            self.signals.attemptUpdateText.emit("Image labeling complete")
            self.signals.finished.emit()

        def frontal(self):
            logging.debug('Front')
            self.store_label('F')
            self.count += 1
            self.display_next_image()
            
        def lateral(self):
            logging.debug('Lateral')
            self.store_label('L')
            self.count += 1
            self.display_next_image()

        def display_next_image(self):
            logging.debug('Image Count: ' + str(self.count))
            self.signals.attemptUpdateText.emit('Image Count: ' + str(self.count))
            self.signals.attemptUpdateProBarValue.emit(self.dbHandler.count_records(self.configHandler.getTableName('label')))

            if self.count < self.expected_num_files:
                self.record = self.records[self.count]
                self.signals.attemptUpdateImage.emit(self.record)
        
        def query_image_list(self):
            logging.debug('Getting the image list')
            sql_query = 'SELECT file_path, bits_stored FROM ' + self.configHandler.getTableName("metadata") + ' ORDER BY file_path;'
            self.records = self.dbHandler.executeQuery(self.dbHandler.connection, sql_query).fetchall()

        def store_label(self, decision):
            logging.debug('Storing label')
            sql_query = 'INSERT INTO ' + self.configHandler.getTableName("label") + ' (file_name, file_path, image_view) VALUES (\'' + self.record['file_path'].split(os.sep)[-1] + '\', \'' + self.record['file_path'] + '\', \'' + decision + '\');'
            self.dbHandler.executeQuery(self.dbHandler.connection, sql_query)
