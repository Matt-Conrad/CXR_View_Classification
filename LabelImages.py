"""Contains the code for the app that helps the user label the data."""
import sys
import psycopg2
import psycopg2.extras
import pydicom as pdm
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtGui import QPixmap, QImage
from config import config
import logging

def run_app(config_file_name):
    """Run application that helps the user label the images."""
    app = QApplication(sys.argv)
    ex = LabelImageApplication(config_file_name)
    sys.exit(app.exec_())

class LabelImageApplication(QWidget):
    """Contains code for the application used to assist in labeling the data."""
    def __init__(self, config_file_name):
        """App constructor.

        Parameters
        ----------
        QWidget : Class
            Application inherits properties from QWidget
        config_file_name : string
            File name of the INI file that contains the config information
        """
        super().__init__()
        
        # Variables
        self.count = 0
        self.conn = None
        self.cur = None # cursor to get image list
        self.cur2 = None # cursor to store labels
        self.config_file_name = config_file_name
        self.label = QLabel(self)
        self.record = None
        # DB Preparation
        self.connect()
        self.query_image_list()
        # Set up GUI
        self.fill_window()

    def __del__(self):
        """On exit of the app close the connection."""
        self.close_connection()
        sys.exit(0)

    def connect(self):
        """Connect the app to the Postgres DB."""
        try:
            logging.info('Opening connection')
            # connect to the PostgreSQL server
            params = config(filename=self.config_file_name, section='postgresql')
            self.conn = psycopg2.connect(**params)
            self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            self.cur2 = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        except (psycopg2.DatabaseError) as error:
            logging.warning(error)

    def close_connection(self):
        """Close the connection set up between the app and the Postgres server."""
        try:
            logging.info('Closing Cursor')
            self.cur.close()
            self.cur2.close()
            logging.info('Cursor closed')
            logging.info('Committing connection')
            self.conn.commit()
            logging.info('Done committing connection')
        except (psycopg2.DatabaseError) as error:
            logging.warning(error)
        finally:
            if self.conn is not None:
                logging.info('Closing connection')
                self.conn.close()
                logging.info('Connection closed')

    def fill_window(self):
        """Displays the content into the window."""
        self.display_next_image()

        frontal_btn = QPushButton('Frontal', self)
        frontal_btn.clicked.connect(self.frontal)
        frontal_btn.move(0, 300)

        lateral_btn = QPushButton('Lateral', self)
        lateral_btn.clicked.connect(self.lateral)
        lateral_btn.move(225, 300)

        self.show()

    def frontal(self):
        """Callback function for the frontal button."""
        self.store_label('F')
        self.display_next_image()

    def lateral(self):
        """Callback function for the lateral button."""
        self.store_label('L')
        self.display_next_image()

    def display_next_image(self):
        """Display the next image."""
        # Get the next available record from the image list query
        self.record = self.cur.fetchone()
        if self.record is None:
            self.__del__()
        # Update the window title with the image count
        self.count += 1
        self.setWindowTitle('Image Count: ' + str(self.count))
        # Read image and update it in the QLabel
        image = pdm.dcmread(self.record['file_path']).pixel_array
        bits_stored = self.record['bits_stored']
        pixmap = self.arr_into_pixmap(image, bits_stored)
        self.label.setPixmap(pixmap)

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
        metadata_table_name = config(filename=self.config_file_name, section='table_info')['metadata_table_name']
        sql_query = 'SELECT file_path, bits_stored FROM ' + metadata_table_name + ' ORDER BY file_path;'
        try:
            logging.info('Getting the image list')
            self.cur.execute(sql_query)
            logging.info('Done getting the image list')
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
        sql_query = 'INSERT INTO image_labels (file_path, label) VALUES (\'' + self.record['file_path'] + '\', \'' + decision + '\');'
        try:
            logging.info('Storing label')
            # create table one by one
            self.cur2.execute(sql_query)
            logging.info('Label is stored')
        except (psycopg2.DatabaseError) as error:
            logging.warning(error)
