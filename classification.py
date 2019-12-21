import numpy as np
import pydicom as pdm
import psycopg2
import psycopg2.extras
import matplotlib.pyplot as plt
import cv2
from config import config
from scipy.ndimage.measurements import label
import time
from skimage.feature import hog
from sklearn import svm
import random
from sklearn.model_selection import KFold, cross_val_score, ShuffleSplit

config_file_name = 'config.ini'
conn = None
try:
    # read the connection parameters
    params = config(filename=config_file_name, section='postgresql')
    table_name = config(filename=config_file_name, section='feature_table_info')['table_name']
    # connect to the PostgreSQL server
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    # Create the SQL query to be used
    sql_query = 'SELECT hor_profile FROM ' + table_name + ' ORDER BY file_path ASC;'
    # create table one by one
    cur.execute(sql_query)
    records = cur.fetchall()
    X1 = [record[0] for record in records]
    X1 = np.array(X1, dtype=np.float)

    sql_query = 'SELECT vert_profile FROM ' + table_name + ' ORDER BY file_path ASC;'
    # create table one by one
    cur.execute(sql_query)
    records = cur.fetchall()
    X2 = [record[0] for record in records]
    X2 = np.array(X2, dtype=np.float)

    X = np.concatenate((X1, X2), axis=1) 

    label_table_name = config(filename=config_file_name, section='label_table_info')['table_name']
    sql_query = 'SELECT label FROM ' + label_table_name + ' ORDER BY file_path ASC;'
    # create table one by one
    cur.execute(sql_query)
    records = cur.fetchall()
    y = [record[0] for record in records]

    # close communication with the PostgreSQL database server
    cur.close()
    # commit the changes
    conn.commit()
except (psycopg2.DatabaseError) as error:
    print(error)
finally:
    if conn is not None:
        conn.close()

# Plot the distributions
# zipped = list(zip(X,y))
# F_nums = [data_point[0] for data_point in zipped if data_point[1] == 'F']
# L_nums = [data_point[0] for data_point in zipped if data_point[1] == 'L']
# plt.hist(F_nums,bins=100,color='r',label='F')
# plt.hist(L_nums,bins=100,color='b',label='L')
# plt.legend()
# plt.show()

kf = KFold(n_splits=10, shuffle=True)

clf = svm.SVC(kernel='linear')
scores = cross_val_score(clf, X, y, cv=kf, scoring='accuracy')

accuracy = np.mean(scores)

print(scores)