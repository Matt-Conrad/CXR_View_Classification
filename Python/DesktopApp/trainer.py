from stage import Stage
from PyQt5.QtCore import pyqtSlot
import logging
import csv
import numpy as np
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn import svm
from joblib import dump

class Trainer(Stage):
    """Class that trains a SVM using the feature vectors and labels, then calculates the accuracy using the test set."""
    def __init__(self, configHandler, dbHandler):
        Stage.__init__(self, configHandler, dbHandler)

    @pyqtSlot()
    def train(self):
        logging.info('Training SVM')

        logging.debug("Extracting feature matrix and labels vector from DB")

        feat_table_name = self.configHandler.getTableName("features")
        sql_query = 'SELECT * FROM ' + feat_table_name + ' ORDER BY file_path ASC;'
        records = self.dbHandler.executeQuery(self.dbHandler.connection, sql_query).fetchall()
        file_names = [record['file_name'] for record in records]
        X1 = [record["hor_profile"] for record in records]
        X2 = [record["vert_profile"] for record in records]

        X1 = np.array(X1, dtype=np.float)
        X2 = np.array(X2, dtype=np.float)
        X = np.concatenate((X1, X2), axis=1)

        sql_query = 'SELECT image_view FROM ' + self.configHandler.getTableName("label") + ' ORDER BY file_path ASC;'
        records = self.dbHandler.executeQuery(self.dbHandler.connection, sql_query).fetchall()
        y = [record[0] for record in records]
        
        logging.debug("Splitting dataset and cross validating SVM for accuracy of classifier")

        X_train, X_test, y_train, y_test, file_names_train, file_names_test = train_test_split(X, y, file_names, test_size=1/3, shuffle=True)

        clf = svm.SVC(kernel='linear')
        n_splits = 10
        if len(X_train) < n_splits:
            kf = KFold(n_splits=len(X_train), shuffle=True)
        else:
            kf = KFold(n_splits=n_splits, shuffle=True)
        scores = cross_val_score(clf, X_train, y_train, cv=kf, scoring='accuracy')

        accuracy = np.mean(scores)

        # Fit the classifier to the full training set, which is 2/3 of the full set as suggested in the paper 
        clf.fit(X_train, y_train)
        test_accuracy = clf.score(X_test, y_test)
        logging.info('Test Set Accuracy: %s', str(test_accuracy))
        
        logging.debug("Saving classifier")
        classifier_file_name = 'full_set_classifier.joblib'
        logging.info('Classifier saved as %s', classifier_file_name)
        dump(clf, classifier_file_name)

        # Save the list of images that are in the test set. You can send these over HTTP to the service.
        image_list_name = "test_images.csv"
        logging.info('A list of images in the test set is saved in %s', image_list_name)
        with open("test_images.csv", "w") as f:
            writer = csv.writer(f)
            for row in file_names_test:
                writer.writerow([row])

        self.attemptUpdateText.emit('K-Fold Cross Validation Accuracy: ' + str(accuracy))
        self.finished.emit()
        logging.info('Done training SVM. K-Fold Cross Validation Accuracy: %s', str(accuracy))