"""Contains the code for the app that helps the user label the data."""
import logging
import os
import psycopg2
import psycopg2.extras
import pydicom as pdm
import cv2
import numpy as np
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import pyqtSignal, pyqtSlot

class Labeler(QWidget):
    """Contains code for the application used to assist in labeling the data."""
    # Signals
    finished = pyqtSignal()
    attemptUpdateProBarValue = pyqtSignal(int)
    attemptUpdateProBarBounds = pyqtSignal(int, int)
    attemptUpdateText = pyqtSignal(str)

    def __init__(self, configHandler, dbHandler):
        """App constructor.

        Parameters
        ----------
        QWidget : Class
            Application inherits properties from QWidget
        config_file_name : string
            File name of the INI file that contains the config information
        """
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
        """On exit of the app close the connection."""
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
        """Callback function for the frontal button."""
        logging.debug('Front')
        self.store_label('F')
        self.display_next_image()

    def lateral(self):
        """Callback function for the lateral button."""
        logging.debug('Lateral')
        self.store_label('L')
        self.display_next_image()

    def display_next_image(self):
        """Display the next image."""
        # Get the next available record from the image list query
        logging.debug('Displaying next image')
        self.record = self.dbHandler.retrieveCursor.fetchone()

        self.attemptUpdateProBarValue.emit(self.dbHandler.count_records(self.configHandler.getTableName('label')))

        if self.record is None:
            logging.info('End of query, deleting labeling app')
            self.close_label_app()
        else:
            # Update the window title with the image count
            self.count += 1
            logging.debug('Image Count: ' + str(self.count))
            self.setWindowTitle('Image Count: ' + str(self.count))
            # Read image and update it in the QLabel
            image = pdm.dcmread(self.record['file_path']).pixel_array
            bits_stored = self.record['bits_stored']
            pixmap = self.arr_into_pixmap(image, bits_stored)
            self.image.setPixmap(pixmap)

    def arr_into_pixmap(self, image, bits_stored):
        """Convert the image array into a QPixmap for display.

        Parameters
        ----------
        image : ndarray
            The image to be converted
        bits_stored : int
            The number of bits stored per pixel (see DICOM documentation)

        Returns
        -------
        QPixmap
            The PYQT5 object with the image embedded in it
        """
        # Scale the pixel intensity to uint8
        highest_possible_intensity = (np.power(2, bits_stored) - 1)
        image = (image/highest_possible_intensity * 255).astype(np.uint8)
        # Resize the image to be 300x300
        image = cv2.resize(image, (300,300), interpolation=cv2.INTER_AREA)
        # Create the QPixmap object
        height, width = image.shape
        bytes_per_line = width
        q_image = QImage(image, width, height, bytes_per_line, QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(q_image)

        return pixmap

    def query_image_list(self):
        """Run a query to get the list of all images in the DB."""
        logging.debug('Attempting to query records for image list')
        sql_query = 'SELECT file_path, bits_stored FROM ' + self.configHandler.getTableName("metadata") + ' ORDER BY file_path;'
        try:
            logging.debug('Getting the image list')
            self.dbHandler.retrieveCursor.execute(sql_query)
            logging.debug('Done getting the image list')
        except (psycopg2.DatabaseError) as error:
            logging.warning(error)

    def store_label(self, decision):
        """Run query that enters the decision into the label table.

        Parameters
        ----------
        decision : string
            The decision of whether the label for the current image is 'L' (lateral) or 'F' (frontal)
        """
        # Create the SQL query to be used
        label_table_name = self.configHandler.getTableName("label")
        sql_query = 'INSERT INTO ' + label_table_name + ' (file_name, file_path, image_view) VALUES (\'' + self.record['file_path'].split(os.sep)[-1] + '\', \'' + self.record['file_path'] + '\', \'' + decision + '\');'
        try:
            logging.debug('Storing label')
            # create table one by one
            self.dbHandler.storeCursor.execute(sql_query)
            logging.debug('Label is stored')
        except (psycopg2.DatabaseError) as error:
            logging.warning(error)
