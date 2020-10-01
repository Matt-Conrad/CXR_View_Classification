from stage import Stage, Runnable
from PyQt5.QtCore import pyqtSlot
import logging
import csv
import numpy as np
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn import svm
from joblib import dump

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

        @pyqtSlot()
        def run(self):
            logging.info('Training SVM')

            self.signals.attemptUpdateText.emit("Training classifier")
            self.signals.attemptUpdateProBarBounds.emit(0, self.expectedNumFiles)
            self.signals.attemptUpdateProBarValue.emit(0)

            logging.debug("Extracting feature matrix and labels vector from DB")

            featTableName = self.configHandler.getTableName("features")
            sqlQuery = 'SELECT * FROM ' + featTableName + ' ORDER BY file_path ASC;'
            records = self.dbHandler.executeQuery(self.dbHandler.connection, sqlQuery).fetchall()
            fileNames = [record['file_name'] for record in records]
            X1 = [record["hor_profile"] for record in records]
            X2 = [record["vert_profile"] for record in records]

            X1 = np.array(X1, dtype=np.float)
            X2 = np.array(X2, dtype=np.float)
            X = np.concatenate((X1, X2), axis=1)

            sqlQuery = 'SELECT image_view FROM ' + self.configHandler.getTableName("label") + ' ORDER BY file_path ASC;'
            records = self.dbHandler.executeQuery(self.dbHandler.connection, sqlQuery).fetchall()
            y = [record[0] for record in records]
            
            logging.debug("Splitting dataset and cross validating SVM for accuracy of classifier")

            XTrain, XTest, yTrain, yTest, fileNamesTrain, fileNamesTest = train_test_split(X, y, fileNames, test_size=1/3, shuffle=True)

            clf = svm.SVC(kernel='linear')
            nSplits = 10
            if len(XTrain) < nSplits:
                kf = KFold(n_splits=len(XTrain), shuffle=True)
            else:
                kf = KFold(n_splits=nSplits, shuffle=True)
            scores = cross_val_score(clf, XTrain, yTrain, cv=kf, scoring='accuracy')

            accuracy = np.mean(scores)

            # Fit the classifier to the full training set, which is 2/3 of the full set as suggested in the paper 
            clf.fit(XTrain, yTrain)
            testAccuracy = clf.score(XTest, yTest)
            logging.info('Test Set Accuracy: %s', str(testAccuracy))
            
            logging.debug("Saving classifier")
            classifierFilename = 'full_set_classifier.joblib'
            logging.info('Classifier saved as %s', classifierFilename)
            dump(clf, classifierFilename)

            # Save the list of images that are in the test set. You can send these over HTTP to the service.
            imageListName = "test_images.csv"
            logging.info('A list of images in the test set is saved in %s', imageListName)
            with open("test_images.csv", "w") as f:
                writer = csv.writer(f)
                for row in fileNamesTest:
                    writer.writerow([row])

            logging.info('Done training SVM. K-Fold Cross Validation Accuracy: %s', str(accuracy))
            self.signals.attemptUpdateText.emit('K-Fold Cross Validation Accuracy: ' + str(accuracy))
            self.signals.attemptUpdateProBarValue.emit(self.expectedNumFiles)
            self.signals.finished.emit()
            