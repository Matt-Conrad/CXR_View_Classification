import logging
import os
import psycopg2
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from stage import Stage

class Labeler(Stage):
    """Class used to assist in labeling the data."""
    attemptUpdateImage = pyqtSignal(object)

    def __init__(self, configHandler, dbHandler):
        Stage.__init__(self, configHandler, dbHandler)

        self.count = 0
        self.record = None
        self.cursor = None

    @pyqtSlot()
    def startLabeler(self):
        """Displays the content into the window."""
        logging.debug('Filling window')
        self.query_image_list()
        
        self.attemptUpdateText.emit("Please manually label images")
        self.attemptUpdateProBarBounds.emit(0, self.expected_num_files)
        self.attemptUpdateProBarValue.emit(0)

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
        self.record = self.cursor.fetchone()

        self.attemptUpdateProBarValue.emit(self.dbHandler.count_records(self.configHandler.getTableName('label')))

        if self.record is None:
            logging.info('End of query')
            self.attemptUpdateText.emit("Image labeling complete")
            self.finished.emit()
        else:
            logging.debug('Image Count: ' + str(self.count))
            if self.count > 0:
                self.attemptUpdateText.emit('Image Count: ' + str(self.count))
            self.attemptUpdateImage.emit(self.record)
            self.count += 1
    
    def query_image_list(self):
        logging.debug('Getting the image list')
        sql_query = 'SELECT file_path, bits_stored FROM ' + self.configHandler.getTableName("metadata") + ' ORDER BY file_path;'
        self.cursor = self.dbHandler.openCursor(self.dbHandler.connection)
        self.dbHandler.executeQuery(self.cursor, sql_query)

    def store_label(self, decision):
        logging.debug('Storing label')
        sql_query = 'INSERT INTO ' + self.configHandler.getTableName("label") + ' (file_name, file_path, image_view) VALUES (\'' + self.record['file_path'].split(os.sep)[-1] + '\', \'' + self.record['file_path'] + '\', \'' + decision + '\');'
        cursor = self.dbHandler.openCursor(self.dbHandler.connection)
        self.dbHandler.executeQuery(cursor, sql_query)
