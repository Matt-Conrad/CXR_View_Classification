from stage import Stage, Runnable
import logging
import os
import pydicom as pdm
from shared_image_processing.features import calc_image_prof
from cxr_pipeline.preprocessing import preprocessing
from PyQt5.QtCore import pyqtSlot
from ctypes import cdll

class FeatCalcStage(Stage):
    """Downloads datasets from online sources."""
    def __init__(self, configHandler, dbHandler):
        Stage.__init__(self)
        self.featureCalculator = self.FeatureCalculator(configHandler, dbHandler)
        self.featCalcUpdater = self.FeatCalcUpdater(configHandler, dbHandler)

    @pyqtSlot()
    def calculateFeatures(self):
        self.threadpool.start(self.featureCalculator)
        self.threadpool.start(self.featCalcUpdater)

    class FeatureCalculator(Runnable):
        """Calculates the feature vectors for each image."""
        def __init__(self, configHandler, dbHandler):
            Runnable.__init__(self, configHandler, dbHandler)

            self.lib = cdll.LoadLibrary("./src/libfeatcalc.so")
            
            self.obj = self.lib.FeatureCalculator_new()

        @pyqtSlot()
        def run(self):
            self.lib.FeatureCalculator_run(self.obj)

    class FeatCalcUpdater(Runnable):
        def __init__(self, configHandler, dbHandler):
            Runnable.__init__(self, configHandler, dbHandler)
            self.featTableName = self.configHandler.getTableName("features")

        @pyqtSlot()
        def run(self):
            self.signals.attemptUpdateText.emit('Calculating features')
            self.signals.attemptUpdateProBarBounds.emit(0, self.expectedNumFiles)
            self.signals.attemptUpdateProBarValue.emit(0)

            while not self.dbHandler.tableExists(self.featTableName):
                pass

            while self.dbHandler.countRecords(self.featTableName) != self.expectedNumFiles:
                self.signals.attemptUpdateProBarValue.emit(self.dbHandler.countRecords(self.featTableName))
                
            self.signals.attemptUpdateProBarValue.emit(self.dbHandler.countRecords(self.featTableName))
            self.signals.attemptUpdateText.emit('Done calculating features')
            self.signals.finished.emit()