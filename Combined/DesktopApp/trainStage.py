from stage import Stage, Runnable
from PyQt5.QtCore import pyqtSlot
import logging
import csv
import numpy as np
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn import svm
from joblib import dump
from ctypes import cdll

class TrainStage(Stage):
    """Downloads datasets from online sources."""
    def __init__(self, configHandler, dbHandler):
        Stage.__init__(self)
        self.trainer = self.Trainer(configHandler, dbHandler)

    @pyqtSlot()
    def train(self):
        self.threadpool.start(self.trainer)

    class Trainer(Runnable):
        """Class that trains a SVM using the feature vectors and labels, then calculates the accuracy using the test set."""
        def __init__(self, configHandler, dbHandler):
            Runnable.__init__(self, configHandler, dbHandler)

            self.lib = cdll.LoadLibrary("./src/libtrainer.so")
            
            self.obj = self.lib.Trainer_new()

        @pyqtSlot()
        def run(self):
            self.signals.attemptUpdateText.emit("Training classifier")
            self.signals.attemptUpdateProBarBounds.emit(0, self.expectedNumFiles)
            self.signals.attemptUpdateProBarValue.emit(0)

            self.lib.Trainer_run(self.obj)

            self.signals.attemptUpdateText.emit('K-Fold Cross Validation Accuracy: Placeholder')
            self.signals.attemptUpdateProBarValue.emit(self.expectedNumFiles)
            self.signals.finished.emit()
            
                
            