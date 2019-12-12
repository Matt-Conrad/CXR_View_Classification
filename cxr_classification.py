"""Contains function that implements 'Orientation Correction for Chest Images'."""

import numpy as np
import pydicom as pdm
import psycopg2
import psycopg2.extras
import matplotlib.pyplot as plt
import cv2
from config import config

def cxr_classification(image):
    """PlaceholderDocstring."""
    

def cycle_thru_table(config_file_name):
    """Cycles through the table and pulls one image at a time."""
    conn = None
    try:
        # read the connection parameters
        params = config(filename=config_file_name, section='postgresql')
        table_name = config(filename=config_file_name, section='table_info')['table_name']
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        # Create the SQL query to be used
        sql_query = 'SELECT * FROM ' + table_name + ' WHERE (window_center IS NOT NULL AND window_width IS NOT NULL);'
        # create table one by one
        cur.execute(sql_query)
        for record in cur:
            # Read the image data
            image = pdm.dcmread(record['file_path']).pixel_array

            image = preprocessing(image, record)

            image_profile = 

            # plt.imshow(image, cmap='bone')
            # plt.show()
            print(record['file_path'])
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def preprocessing(image, record):
    """Placholder."""
    highest_possible_intensity = (np.power(2, record['bits_stored']) - 1)
    image_norm = image/highest_possible_intensity

    # window_center = record['window_center']/highest_possible_intensity
    # window_width = record['window_width']/highest_possible_intensity
    # min_I = window_center - (window_width/2)
    # max_I = window_center + (window_width/2)

    # image_norm = contrast_stretch(image_norm, min_I, max_I)

    # Invert the image if it's MONOCHROME1
    if record['photometric_interpretation'] == 'MONOCHROME1':
        image_norm = 1 - image_norm
    elif record['photometric_interpretation'] == 'MONOCHROME2':
        pass
    else:
        raise ValueError('Image is not MONOCHROME1 or MONOCHROME2 as expected.')

    saturation_vals = np.percentile(image_norm.flatten(), [1, 99])

    image_enhanced = contrast_stretch(image_norm, saturation_vals[0], saturation_vals[1])

    median = np.median(image_enhanced)
    
    image_binarized = (image_enhanced >= median).astype(np.uint8)

    # get the bounding rect
    x, y, w, h = cv2.boundingRect(image_binarized)
    # draw a green rectangle to visualize the bounding rect
    image_enh_copy = image_enhanced.copy()
    cv2.rectangle(image_enh_copy, (x, y), (x+w, y+h), 1, 2)

    image_cropped = image_enhanced[y:y+h, x:x+w]

    scale_percent = .5
    width = int(image_cropped.shape[1] * scale_percent)
    height = int(image_cropped.shape[0] * scale_percent)
    dim = (width, height)
    image_downsize = cv2.resize(image_cropped, dim, interpolation=cv2.INTER_AREA)

    # plt.subplot(1,2,1)
    # plt.imshow(image_cropped, cmap='bone')
    # plt.subplot(1,2,2)
    # plt.imshow(image_downsize, cmap='bone')
    # plt.show()
    print(record['file_path'])
    
    return image_downsize

def contrast_stretch(image, min_I, max_I):
    """Placeholder."""
    # All values < min_I will be 0 and all values > max_I will be 1
    image_copy = image.copy()
    image_copy[np.where(image < min_I)] = 0
    image_copy[np.where(image > max_I)] = 1

    A = np.array([[min_I, 1], [max_I, 1]])
    B = [0, 1]
    [slope, intercept] = np.linalg.solve(A, B)

    image_copy[np.where((image_copy >= min_I) & (image_copy <= max_I))] = \
        slope * image_copy[np.where((image_copy >= min_I) & (image_copy <= max_I))] + intercept

    return image_copy

if __name__ == '__main__':
    cycle_thru_table('config.ini')