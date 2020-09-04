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

        # Get all file names of dataset
        feat_table_name = self.configHandler.getTableName("features")
        sql_query = 'SELECT file_name FROM ' + feat_table_name + ' ORDER BY file_path ASC;'
        self.dbHandler.executeQuery(self.dbHandler.retrieveCursor, sql_query)
        records = self.dbHandler.retrieveCursor.fetchall()
        file_names = [record[0] for record in records]

        # Put all horizontal profiles into feature matrix
        sql_query = 'SELECT hor_profile FROM ' + feat_table_name + ' ORDER BY file_path ASC;'
        self.dbHandler.executeQuery(self.dbHandler.retrieveCursor, sql_query)
        records = self.dbHandler.retrieveCursor.fetchall()
        X1 = [record[0] for record in records]
        X1 = np.array(X1, dtype=np.float)

        # Put all vertical profiles into feature matrix
        sql_query = 'SELECT vert_profile FROM ' + feat_table_name + ' ORDER BY file_path ASC;'
        self.dbHandler.executeQuery(self.dbHandler.retrieveCursor, sql_query)
        records = self.dbHandler.retrieveCursor.fetchall()
        X2 = [record[0] for record in records]
        X2 = np.array(X2, dtype=np.float)

        X = np.concatenate((X1, X2), axis=1) 

        # Put all the labels into a list
        sql_query = 'SELECT image_view FROM ' + self.configHandler.getTableName("label") + ' ORDER BY file_path ASC;'
        self.dbHandler.executeQuery(self.dbHandler.retrieveCursor, sql_query)
        records = self.dbHandler.retrieveCursor.fetchall()
        y = [record[0] for record in records]
        
        # Split the dataset into 2/3 training 1/3 testing
        X_train, X_test, y_train, y_test, file_names_train, file_names_test = train_test_split(X, y, file_names, test_size=1/3, shuffle=True)

        # Cross validate with the linear SVM, and calculate accuracy
        clf = svm.SVC(kernel='linear')
        n_splits = 10
        if len(X_train) < n_splits:
            kf = KFold(n_splits=len(X_train), shuffle=True)
        else:
            kf = KFold(n_splits=n_splits, shuffle=True)
        scores = cross_val_score(clf, X_train, y_train, cv=kf, scoring='accuracy')

        # Calculate the accuracy of the classifier estimated by the K-Fold cross validation
        accuracy = np.mean(scores)
        logging.info('K-Fold Cross Validation Accuracy: %s', str(accuracy))

        # Fit the classifier to the full training set, which is 2/3 of the full set as suggested in the paper 
        clf.fit(X_train, y_train)
        test_accuracy = clf.score(X_test, y_test)
        logging.info('Test Set Accuracy: %s', str(test_accuracy))
        
        # Save the classifier by overwriting the previous classifier if it exists
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