from stage import Stage, Runnable
import logging
import os
import pydicom as pdm
from shared_image_processing.features import calc_image_prof
from cxr_pipeline.preprocessing import preprocessing
from PyQt5.QtCore import pyqtSlot

import time

class FeatCalcStage(Stage):
    """Downloads datasets from online sources."""
    def __init__(self, configHandler, dbHandler):
        Stage.__init__(self)
        self.featureCalculator = self.FeatureCalculator(configHandler, dbHandler)

    @pyqtSlot()
    def calculateFeatures(self):
        self.threadpool.start(self.featureCalculator)

    class FeatureCalculator(Runnable):
        """Calculates the feature vectors for each image."""
        def __init__(self, configHandler, dbHandler):
            Runnable.__init__(self, configHandler, dbHandler)
            self.featTableName = self.configHandler.getTableName("features")

        @pyqtSlot()
        def run(self):
            start = time.time()
            logging.info('Calculating features from images')
            
            sqlQuery = 'SELECT * FROM ' + self.configHandler.getTableName("metadata") + ';'
            records = self.dbHandler.executeQuery(self.dbHandler.connection, sqlQuery).fetchall()
            self.dbHandler.addTableToDb(self.featTableName, self.configHandler.getColumnsInfoFullPath(), "nonElementColumns", 'features_list')

            self.signals.attemptUpdateText.emit('Calculating features')
            self.signals.attemptUpdateProBarBounds.emit(0, self.expectedNumFiles)
            self.signals.attemptUpdateProBarValue.emit(self.dbHandler.countRecords(self.featTableName))

            count = 0
            for record in records:
                filePath = record['file_path']
                fileFullPath = os.path.join(self.configHandler.getParentFolder(), filePath)
                count += 1
                logging.debug('Calculating for image number: %s File: %s', str(count), fileFullPath)
                image = pdm.dcmread(fileFullPath).pixel_array
                
                image = preprocessing(image, record['bits_stored'], record['photometric_interpretation'])

                (horProfile, vertProfile) = calc_image_prof(image)

                self.store(filePath, horProfile, vertProfile)
                self.signals.attemptUpdateProBarValue.emit(self.dbHandler.countRecords(self.featTableName))

            logging.info('Done calculating features from images')
            end = time.time()
            print(end - start)
            self.signals.attemptUpdateText.emit('Done calculating features')
            self.signals.finished.emit()

        def store(self, filePath, horProfile, vertProfile):
            logging.debug('Storing the calculated features into the database.')
            sqlQuery = 'INSERT INTO ' + self.configHandler.getTableName("features") + ' (file_name, file_path, hor_profile, vert_profile) VALUES (%s, %s, %s, %s);'

            values = (filePath.split(os.sep)[-1], filePath, horProfile.tolist(), vertProfile.tolist())
            self.dbHandler.executeQuery(self.dbHandler.connection, sqlQuery, values)
        