from stage import Stage
import logging
import os
import pydicom as pdm
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
        
        sql_query = 'SELECT * FROM ' + self.configHandler.getTableName("metadata") + ';'
        records = self.dbHandler.executeQuery(self.dbHandler.connection, sql_query, fetchHowMany="all")
        self.dbHandler.add_table_to_db(self.featTableName, self.configHandler.getColumnsInfoPath(), 'features_list')

        self.attemptUpdateText.emit('Calculating features')
        self.attemptUpdateProBarBounds.emit(0, self.expected_num_files)
        self.attemptUpdateProBarValue.emit(self.dbHandler.count_records(self.featTableName))

        count = 0
        for record in records:
            file_path = record['file_path']
            count += 1
            logging.debug('Calculating for image number: %s File: %s', str(count), file_path)
            image = pdm.dcmread(file_path).pixel_array
            
            image = preprocessing(image, record['bits_stored'], record['photometric_interpretation'])

            (hor_profile, vert_profile) = calc_image_prof(image)

            self.store(self.configHandler.getConfigFilename(), file_path, hor_profile, vert_profile)

            self.attemptUpdateProBarValue.emit(self.dbHandler.count_records(self.featTableName))

        self.attemptUpdateText.emit('Done calculating features')
        self.finished.emit()
        logging.info('Done calculating features from images')

    def store(self, config_file_name, file_path, hor_profile, vert_profile):
        logging.debug('Storing the calculated features into the database.')
        sql_query = 'INSERT INTO ' + self.configHandler.getTableName("features") + ' (file_name, file_path, hor_profile, vert_profile) VALUES (%s, %s, %s, %s);'

        values = (file_path.split(os.sep)[-1], file_path, hor_profile.tolist(), vert_profile.tolist())
        self.dbHandler.executeQuery(self.dbHandler.connection, sql_query, values)
    