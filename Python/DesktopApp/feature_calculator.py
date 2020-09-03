from stage import Stage
import logging
import os
import pydicom as pdm
import psycopg2
import psycopg2.extras
from shared_image_processing.features import calc_image_prof
from cxr_pipeline.preprocessing import preprocessing
from PyQt5.QtCore import pyqtSlot

class FeatureCalculator(Stage):
    """Calculates the feature vectors for each image."""
    def __init__(self, configHandler, dbHandler):
        Stage.__init__(self, configHandler, dbHandler)
        self.featTableName = self.configHandler.getTableName("features")

    @pyqtSlot()
    def calculate_features(self):
        logging.info('Calculating features from images')
        conn = None
        try:
            table_name = self.configHandler.getTableName("metadata")
            logging.debug('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(**self.configHandler.getDbInfo())
            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            logging.debug('Connection established')
            sql_query = 'SELECT * FROM ' + table_name + ';'
            cur.execute(sql_query)
            count = 0

            self.dbHandler.add_table_to_db(self.featTableName, self.configHandler.getColumnsInfoPath(), 'features_list')
            
            self.attemptUpdateText.emit('Calculating features')
            self.attemptUpdateProBarBounds.emit(0, self.expected_num_files)
            self.attemptUpdateProBarValue.emit(self.dbHandler.count_records(self.featTableName))

            for record in cur:
                file_path = record['file_path']
                count += 1
                logging.info('Calculating for image number: %s File: %s', str(count), file_path)
                image = pdm.dcmread(file_path).pixel_array
                
                image = preprocessing(image, record['bits_stored'], record['photometric_interpretation'])

                (hor_profile, vert_profile) = calc_image_prof(image)

                self.store(self.configHandler.getConfigFilename(), file_path, hor_profile, vert_profile)

                self.attemptUpdateProBarValue.emit(self.dbHandler.count_records(self.featTableName))

            cur.close()
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
        logging.debug('Storing the calculated features into the database.')
        conn = None
        try:
            out_table_name = self.configHandler.getTableName("features")
            conn = psycopg2.connect(**self.configHandler.getDbInfo())
            cur = conn.cursor()
            sql_query = 'INSERT INTO ' + out_table_name + ' (file_name, file_path, hor_profile, vert_profile) VALUES (%s, %s, %s, %s);'
            values = (file_path.split(os.sep)[-1], file_path, hor_profile.tolist(), vert_profile.tolist())
            cur.execute(sql_query, values)

            cur.close()
            conn.commit()
        except (psycopg2.DatabaseError) as error:
            logging.warning(error)
        finally:
            if conn is not None:
                conn.close()
                logging.debug('Done storing.')
    