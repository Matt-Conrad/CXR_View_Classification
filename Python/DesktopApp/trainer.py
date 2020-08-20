from stage import Stage
from PyQt5.QtCore import pyqtSlot
from LabelImages import LabelImageApplication
import logging
import csv
import numpy as np
import psycopg2
import psycopg2.extras
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn import svm
from joblib import dump
from metadata_to_db.config import config

class Trainer(Stage):
    """Controls logic of getting the dataset from online sources."""
    def __init__(self, configHandler, dbHandler):
        Stage.__init__(self, configHandler, dbHandler)

    @pyqtSlot()
    def train(self):
        """Train a SVM using the feature vectors and labels, then calculate the accuracy using the test set.
        
        Parameters
        ----------
        config_file_name : string
            File name of the INI file with DB and folder config information
        
        Returns
        -------
        (sklearn classifier, float)
            The trained classifier and the corresponding accuracy
        """
        logging.info('***BEGIN CLASSIFICATION PHASE***')
        logging.info('Running classification')
        conn = None
        try:
            # read the connection parameters
            params = config(filename=self.configHandler.getConfigFilename(), section='postgresql')
            table_name = config(filename=self.configHandler.getConfigFilename(), section='table_info')['features_table_name']

            # connect to the PostgreSQL server
            conn = psycopg2.connect(**params)
            cur = conn.cursor()

            # Put all horizontal profiles into feature matrix
            sql_query = 'SELECT file_name FROM ' + table_name + ' ORDER BY file_path ASC;'
            cur.execute(sql_query)
            records = cur.fetchall()
            file_names = [record[0] for record in records]

            # Put all horizontal profiles into feature matrix
            sql_query = 'SELECT hor_profile FROM ' + table_name + ' ORDER BY file_path ASC;'
            cur.execute(sql_query)
            records = cur.fetchall()
            X1 = [record[0] for record in records]
            X1 = np.array(X1, dtype=np.float)

            # Put all vertical profiles into feature matrix
            sql_query = 'SELECT vert_profile FROM ' + table_name + ' ORDER BY file_path ASC;'
            cur.execute(sql_query)
            records = cur.fetchall()
            X2 = [record[0] for record in records]
            X2 = np.array(X2, dtype=np.float)

            # Combine the 2 matrices, making feature vectors twice as long
            X = np.concatenate((X1, X2), axis=1) 

            # Put all the labels into a list
            label_table_name = config(filename=self.configHandler.getConfigFilename(), section='table_info')['label_table_name']
            sql_query = 'SELECT image_view FROM ' + label_table_name + ' ORDER BY file_path ASC;'
            cur.execute(sql_query)
            records = cur.fetchall()
            y = [record[0] for record in records]

            # close communication with the PostgreSQL database server
            cur.close()
            # commit the changes
            conn.commit()
        except (psycopg2.DatabaseError) as error:
            logging.info(error)
        finally:
            if conn is not None:
                conn.close()
        
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
        logging.info('***END CLASSIFICATION PHASE***')