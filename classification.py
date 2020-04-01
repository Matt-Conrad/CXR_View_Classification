"""Contains function for training and predicting with the classifier."""
import logging
import pickle
import numpy as np
import psycopg2
import psycopg2.extras
from sklearn.model_selection import KFold, cross_val_score
from sklearn import svm
from joblib import dump
from DicomToDatabase.config import config

def classification(config_file_name):
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
    logging.info('Running classification')
    conn = None
    try:
        # read the connection parameters
        params = config(filename=config_file_name, section='postgresql')
        table_name = config(filename=config_file_name, section='table_info')['features_table_name']

        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

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
        label_table_name = config(filename=config_file_name, section='table_info')['label_table_name']
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
    
    # Cross validate with the linear SVM, and calculate accuracy
    kf = KFold(n_splits=10, shuffle=True)

    clf = svm.SVC(kernel='linear')
    scores = cross_val_score(clf, X, y, cv=kf, scoring='accuracy')

    accuracy = np.mean(scores)
    # clf.fit(X, y)
    logging.info('Done classifying: %s', str(accuracy))
    # dump(clf, 'full_set_classifier.joblib') 
    return clf, accuracy