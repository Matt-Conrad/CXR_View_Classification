import logging
import os
import psycopg2
import pydicom as pdm
import cv2
import numpy as np
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import pyqtSignal, pyqtSlot

class Labeler(QWidget):
    """Contains code for the application used to assist in labeling the data."""
    finished = pyqtSignal()
    attemptUpdateProBarValue = pyqtSignal(int)
    attemptUpdateProBarBounds = pyqtSignal(int, int)
    attemptUpdateText = pyqtSignal(str)

    def __init__(self, configHandler, dbHandler):
        logging.info('Constructing Labeling app')
        super().__init__()
        
        self.configHandler = configHandler
        self.dbHandler = dbHandler

        self.count = 0

        # Variables
        self.record = None

        self.image = QLabel(self)
        self.frontal_btn = QPushButton('Frontal', self)
        self.lateral_btn = QPushButton('Lateral', self)
        
        logging.info('Done constructing Labeling app')
        
    def close_label_app(self):
        logging.info('Attempting to close connection')
        self.dbHandler.closeConnection()
        self.attemptUpdateText.emit("Image labeling complete")
        self.finished.emit()
        self.close()
        logging.info('Closing Labeling app')

    @pyqtSlot()
    def fill_window(self):
        """Displays the content into the window."""
        logging.debug('Filling window')
        self.query_image_list()
        self.attemptUpdateText.emit("Please manually label images")
        self.dbHandler.add_table_to_db(self.configHandler.getTableName('label'), self.configHandler.getColumnsInfoPath(), 'labels')
        
        layout = QGridLayout()

        layout.addWidget(self.image, 1, 0, 1, 2)
        layout.addWidget(self.frontal_btn, 2, 0)
        layout.addWidget(self.lateral_btn, 2, 1)

        self.setLayout(layout)
        self.display_next_image()
        self.frontal_btn.clicked.connect(self.frontal)
        self.lateral_btn.clicked.connect(self.lateral)
        self.show()

        logging.debug('Done filling window')

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
        self.record = self.queryCursor.fetchone()

        self.attemptUpdateProBarValue.emit(self.dbHandler.count_records(self.configHandler.getTableName('label')))

        if self.record is None:
            logging.info('End of query, deleting labeling app')
            self.close_label_app()
        else:
            # Update the window title and image
            self.count += 1
            logging.debug('Image Count: ' + str(self.count))
            self.setWindowTitle('Image Count: ' + str(self.count))

            image = pdm.dcmread(self.record['file_path']).pixel_array
            bits_stored = self.record['bits_stored']
            pixmap = self.arr_into_pixmap(image, bits_stored)
            self.image.setPixmap(pixmap)

    def arr_into_pixmap(self, image, bits_stored):
        """Convert the image array into a QPixmap for display."""
        # Scale the pixel intensity to uint8
        highest_possible_intensity = (np.power(2, bits_stored) - 1)
        image = (image/highest_possible_intensity * 255).astype(np.uint8)

        image = cv2.resize(image, (300,300), interpolation=cv2.INTER_AREA)

        height, width = image.shape
        bytes_per_line = width
        q_image = QImage(image, width, height, bytes_per_line, QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(q_image)

        return pixmap

    def query_image_list(self):
        logging.debug('Attempting to query records for image list')
        sql_query = 'SELECT file_path, bits_stored FROM ' + self.configHandler.getTableName("metadata") + ' ORDER BY file_path;'
        self.queryCursor = self.dbHandler.openCursor(self.dbHandler.connection)
        try:
            logging.debug('Getting the image list')
            self.queryCursor.execute(sql_query)
            logging.debug('Done getting the image list')
        except (psycopg2.DatabaseError) as error:
            logging.warning(error)

    def store_label(self, decision):
        logging.debug('Storing label')
        sql_query = 'INSERT INTO ' + self.configHandler.getTableName("label") + ' (file_name, file_path, image_view) VALUES (\'' + self.record['file_path'].split(os.sep)[-1] + '\', \'' + self.record['file_path'] + '\', \'' + decision + '\');'
        self.dbHandler.executeQuery(self.dbHandler.storeCursor, sql_query)
