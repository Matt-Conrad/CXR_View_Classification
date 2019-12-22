"""Placeholder."""
from config import config
import psycopg2
import psycopg2.extras
import pydicom as pdm
import basic_db_ops as bdo
import matplotlib.pyplot as plt
import sys
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton
from PyQt5.QtGui import QIcon, QPixmap, QImage
import numpy as np

def run_app():
    app = QApplication(sys.argv)
    ex = App('config.ini')
    sys.exit(app.exec_())

class App(QWidget):
    def __init__(self,config_file_name):
        super().__init__()
        self.title = 'PyQt5 simple window'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.count = 0
        self.conn = None
        self.cur = None
        self.cur2 = None
        self.table_name = config(filename=config_file_name, section='table_info')['table_name']
        self.params = config(filename=config_file_name, section='postgresql')
        self.label = None
        self.record = None
        self.initUI()

    def __del__(self):
        self.close_connection()
 
    def initUI(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.connect()
        self.run_query()
        self.display()    

    def connect(self):
        try:
            print('Opening connection')
            # connect to the PostgreSQL server
            self.conn = psycopg2.connect(**self.params)
            self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            self.cur2 = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        except (psycopg2.DatabaseError) as error:
            print(error)

    def run_query(self):
        # Create the SQL query to be used
        sql_query = 'SELECT file_path, bits_stored FROM ' + self.table_name + ' ORDER BY file_path;'
        try:
            print('Running query')
            # create table one by one
            self.cur.execute(sql_query)
        except (psycopg2.DatabaseError) as error:
            print(error)

    def run_query2(self, decision):
        # Create the SQL query to be used
        sql_query = 'INSERT INTO image_labels (file_path, label) VALUES (\'' + self.record['file_path'] + '\', \'' + decision + '\');'
        try:
            print('Running query')
            # create table one by one
            self.cur2.execute(sql_query)
        except (psycopg2.DatabaseError) as error:
            print(error)

    def display(self):
        self.label = QLabel(self)
        self.record = self.cur.fetchone()
        self.display_image()

        front_btn = QPushButton('Frontal', self)
        front_btn.resize(front_btn.sizeHint())
        front_btn.clicked.connect(self.frontal)
        front_btn.move(0, 300)

        btn = QPushButton('Lateral', self)
        btn.resize(btn.sizeHint())
        btn.clicked.connect(self.lateral)
        btn.move(225, 300)

        self.show()

    def frontal(self):
        self.run_query2('F')
        self.record = self.cur.fetchone()
        if self.record is None:
            sys.exit()
        self.display_image()

    def lateral(self):
        self.run_query2('L')
        self.record = self.cur.fetchone()
        if self.record is None:
            sys.exit()
        self.display_image()

    def close_connection(self):
        try:
            print('Closing Cursor and commiting changes')
            # close communication with the PostgreSQL database server
            self.cur.close()
            # commit the changes
            self.conn.commit()
        except (psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if self.conn is not None:
                print('Closing connection')
                self.conn.close()

    def display_image(self):
        # Read the image data
        image = pdm.dcmread(self.record['file_path']).pixel_array
        bits_stored = self.record['bits_stored']
        pixmap = self.arr_into_pixmap(image, bits_stored)
        self.count += 1
        self.setWindowTitle(str(self.count))

        self.label.setPixmap(pixmap)

    def arr_into_pixmap(self, image, bits_stored):
        highest_possible_intensity = (np.power(2, bits_stored) - 1)
        image = (image/highest_possible_intensity * 255).astype(np.uint8)

        image = cv2.resize(image, (300,300), interpolation=cv2.INTER_AREA)

        height, width = image.shape
        bytesPerLine = width
        qImg = QImage(image, width, height, bytesPerLine, QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(qImg)

        return pixmap

if __name__ == '__main__':
    # bdo.drop_table('image_labels', 'config.ini')
    # bdo.add_table_to_db('image_labels', 'elements.json', 'config.ini')

    app = QApplication(sys.argv)
    ex = App('config.ini')
    sys.exit(app.exec_())
