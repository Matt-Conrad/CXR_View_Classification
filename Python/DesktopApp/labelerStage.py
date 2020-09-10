import logging
import os
import psycopg2
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from stage import Stage, Runnable

class LabelerStage(Stage):
    """Downloads datasets from online sources."""
    def __init__(self, configHandler, dbHandler):
        Stage.__init__(self)
        self.labeler = self.Labeler(configHandler, dbHandler)

    @pyqtSlot()
    def label(self):
        # self.threadpool.start(self.labeler)
        self.labeler.run()

    class Labeler(Runnable):
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

        def frontal(self):
            logging.debug('Front')
            self.store_label('F')
            self.display_next_image()

        def lateral(self):
            logging.debug('Lateral')
            self.store_label('L')
            self.display_next_image()

        def display_next_image(self):
            logging.debug('Displaying next image')
            self.signals.attemptUpdateProBarValue.emit(self.dbHandler.count_records(self.configHandler.getTableName('label')))

            if self.count == self.expected_num_files:
                logging.info('End of query')
                self.signals.attemptUpdateText.emit("Image labeling complete")
                self.signals.finished.emit()
            else:
                logging.debug('Image Count: ' + str(self.count))
                self.record = self.records[self.count]
                if self.count > 0:
                    self.signals.attemptUpdateText.emit('Image Count: ' + str(self.count))
                self.signals.attemptUpdateImage.emit(self.record)
                self.count += 1
        
        def query_image_list(self):
            logging.debug('Getting the image list')
            sql_query = 'SELECT file_path, bits_stored FROM ' + self.configHandler.getTableName("metadata") + ' ORDER BY file_path;'
            self.records = self.dbHandler.executeQuery(self.dbHandler.connection, sql_query).fetchall()

        def store_label(self, decision):
            logging.debug('Storing label')
            sql_query = 'INSERT INTO ' + self.configHandler.getTableName("label") + ' (file_name, file_path, image_view) VALUES (\'' + self.record['file_path'].split(os.sep)[-1] + '\', \'' + self.record['file_path'] + '\', \'' + decision + '\');'
            self.dbHandler.executeQuery(self.dbHandler.connection, sql_query)
