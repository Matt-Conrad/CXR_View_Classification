"""Contains script that moves all DCM tag-values from a directory of DCMs into a PostgreSQL DB."""
from stage import Stage
import logging
import os
# import time
import numpy as np
import pydicom as pdm
import psycopg2
import psycopg2.extras
# import matplotlib.pyplot as plt
# from scipy.ndimage.measurements import label
from metadata_to_db.config import config
from shared_image_processing.features import calc_image_prof
from cxr_pipeline.preprocessing import preprocessing
from PyQt5.QtCore import pyqtSlot

class FeatureCalculator(Stage):
    """Controls logic of getting the dataset from online sources."""
    def __init__(self, configHandler, dbHandler):
        Stage.__init__(self, configHandler, dbHandler)
        self.featTableName = self.configHandler.getTableName("features")

    @pyqtSlot()
    def calculate_features(self):
        """Cycles through the table and pulls one image at a time.
        
        Parameters
        ----------
        config_file_name : string
            The INI file with DB and folder configuration information
        """
        logging.info('Calculating features from images')
        conn = None
        try:
            # read the connection parameters
            params = self.configHandler.getDbInfo()
            table_name = self.configHandler.getTableName("metadata")
            # connect to the PostgreSQL server
            logging.debug('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(**params)
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            logging.debug('Connection established')
            # Create the SQL query to be used
            sql_query = 'SELECT * FROM ' + table_name + ';'
            # create table one by one
            cur.execute(sql_query)
            count = 0

            # Add table to DB
            self.dbHandler.add_table_to_db(self.featTableName, self.configHandler.getColumnsInfoPath(), 'features_list')
            
            # Set the progress region
            self.attemptUpdateText.emit('Calculating features')
            self.attemptUpdateProBarBounds.emit(0, self.expected_num_files)
            self.attemptUpdateProBarValue.emit(self.dbHandler.count_records(self.featTableName))

            for record in cur:
                # Read the image data
                file_path = record['file_path']
                count += 1
                logging.info('Calculating for image number: %s File: %s', str(count), file_path)
                image = pdm.dcmread(file_path).pixel_array
                
                # Preprocess the image
                image = preprocessing(image, record['bits_stored'], record['photometric_interpretation'])

                # Calculate the various features
                (hor_profile, vert_profile) = calc_image_prof(image)

                # Store the data to the DB
                self.store(self.configHandler.getConfigFilename(), file_path, hor_profile, vert_profile)

                self.attemptUpdateProBarValue.emit(self.dbHandler.count_records(self.featTableName))

            # close communication with the PostgreSQL database server
            cur.close()
            # commit the changes
            conn.commit()
        except (psycopg2.DatabaseError) as error:
            logging.warning(error)
        finally:
            if conn is not None:
                conn.close()
                self.attemptUpdateText.emit('Done calculating features')
                self.finished.emit()
                logging.info('Done calculating features from images')

    def store(self, config_file_name, file_path, hor_profile, vert_profile):
        """Stores the calculated features into the database.
        
        Parameters
        ----------
        config_file_name : string
            The INI file with DB and folder configuration information
        file_path : string
            Path to the image file
        ratio : float
            Ratio of torso dimensions
        hor_profile : float[]
            Vector containing horizontal profile of torso
        vert_profile : float[]
            Vector containing vertical profile of torso
        pyr_hog : float[]
            Vector containing the pyramid HOG
        """
        logging.debug('Storing the calculated features into the database.')
        conn = None
        try:
            # read the connection parameters
            params = config(filename=config_file_name, section='postgresql')
            out_table_name = config(filename=config_file_name, section='table_info')['features_table_name']
            # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            # Create the SQL query to be used
            sql_query = 'INSERT INTO ' + out_table_name + ' (file_name, file_path, hor_profile, vert_profile) VALUES (%s, %s, %s, %s);'
            values = (file_path.split(os.sep)[-1], file_path, hor_profile.tolist(), vert_profile.tolist())
            # create table one by one
            cur.execute(sql_query, values)

            cur.close()
            # commit the changes
            conn.commit()
        except (psycopg2.DatabaseError) as error:
            logging.warning(error)
        finally:
            if conn is not None:
                conn.close()
                logging.debug('Done storing.')
    