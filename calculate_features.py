"""Contains function that implements 'Orientation Correction for Chest Images'."""

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

def calculate_features(config_file_name):
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
        sql_query = 'SELECT * FROM ' + table_name + ';'
        # create table one by one
        cur.execute(sql_query)
        count = 0
        for record in cur:
            # Read the image data
            image = pdm.dcmread(record['file_path']).pixel_array
            
            image = preprocessing(image, record)

            # Profile features
            (hor_profile, vert_profile) = calc_image_prof(image)
            
            ratio = calc_body_size_ratio(image)
            
            phog_vector = phog(image, n_bins=8, orient_range=(0, 360), levels=3)

            store('config.ini', record['file_path'], ratio, hor_profile, vert_profile, phog_vector)

            count += 1
            print('Number: ' + str(count) + ' File: ' + record['file_path'])
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def store(config_file_name, file_path, ratio, hor_profile, vert_profile, phog):
    """Placeholder."""
    conn = None
    try:
        # read the connection parameters
        params = config(filename=config_file_name, section='postgresql')
        out_table_name = config(filename=config_file_name, section='feature_table_info')['table_name']
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # Create the SQL query to be used
        sql_query = 'INSERT INTO ' + out_table_name + ' (file_path, body_size_ratio, hor_profile, vert_profile, phog) VALUES (%s, %s, %s, %s, %s);'
        values = (file_path, ratio, hor_profile.tolist(), vert_profile.tolist(), phog.tolist())
        # create table one by one
        cur.execute(sql_query, values)

        cur.close()
        # commit the changes
        conn.commit()
    except (psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def phog(image, n_bins, orient_range, levels):
    """Placeholder."""
    # Going with this for now. If this doesn't work for some reason, try the cv2 one or try the
    # imlementation of it at:
    # https://github.com/ReseachWithDrSun/test/blob/fdae985309e488de42b7ac3c88306345b2d739e7/dtyu/xray_learning/phog_features/phog.py

    # NOTE: might need to include some form of Canny edge detector in here somewhere

    feature_vector0, hog_image0 = hog(image, orientations=n_bins, pixels_per_cell=image.shape, cells_per_block=(1, 1),
                                    visualize=True, feature_vector=True)

    cell_size = (int(image.shape[0]/2), int(image.shape[1]/2))
    feature_vector1, hog_image1 = hog(image, orientations=n_bins, pixels_per_cell=cell_size, 
                                    cells_per_block=(1, 1), visualize=True, feature_vector=True)

    cell_size = (int(image.shape[0]/4), int(image.shape[1]/4))
    feature_vector2, hog_image2 = hog(image, orientations=n_bins, pixels_per_cell=cell_size, 
                                    cells_per_block=(1, 1), visualize=True, feature_vector=True)

    cell_size = (int(image.shape[0]/8), int(image.shape[1]/8))
    feature_vector3, hog_image3 = hog(image, orientations=n_bins, pixels_per_cell=cell_size, 
                                    cells_per_block=(1, 1), visualize=True, feature_vector=True)
    # NOTE: The size of the output descriptor is exactly the length from the paper: 8 + 32 + 128 + 512 = 680
    # plt.subplot(1, 5, 1)
    # plt.imshow(image, cmap='bone')
    # plt.subplot(1, 5, 2)
    # plt.imshow(hog_image0, cmap='bone')
    # plt.subplot(1, 5, 3)
    # plt.imshow(hog_image1, cmap='bone')
    # plt.subplot(1, 5, 4)
    # plt.imshow(hog_image2, cmap='bone')
    # plt.subplot(1, 5, 5)
    # plt.imshow(hog_image3, cmap='bone')
    # plt.show()

    return np.concatenate((feature_vector0, feature_vector1, feature_vector2, feature_vector3))


def calc_body_size_ratio(image):
    """Placeholder."""
    median = np.median(image)
    image_binarized = (image >= median).astype(np.uint8)

    comp = getBiggestComp(image_binarized)

    first_nonzeros_hor = first_nonzero(comp, axis=1, invalid_val=np.nan)
    last_nonzeros_hor = last_nonzero(comp, axis=1, invalid_val=np.nan)

    first_nonzeros_vert = first_nonzero(comp, axis=0, invalid_val=np.nan)
    last_nonzeros_vert = last_nonzero(comp, axis=0, invalid_val=np.nan)

    hor_cross_sections = last_nonzeros_hor - first_nonzeros_hor
    vert_cross_sections = last_nonzeros_vert - first_nonzeros_vert

    hor_median = np.nanmedian(hor_cross_sections)
    vert_max = np.nanmax(vert_cross_sections)
    vert_max_ind = np.nanargmax(vert_cross_sections)
    hor_median_ind = np.argsort(hor_cross_sections)[len(hor_cross_sections)//2]

    ratio = hor_median/vert_max

    # plt.subplot(1, 3, 1)
    # plt.imshow(image, cmap='bone')
    # plt.subplot(1, 3, 2)
    # plt.imshow(comp, cmap='bone')
    # plt.plot(first_nonzeros_hor, np.arange(0, image.shape[0]), 'r.')
    # plt.plot(last_nonzeros_hor, np.arange(0, image.shape[0]), 'r.')
    # plt.plot([first_nonzeros_hor[hor_median_ind], last_nonzeros_hor[hor_median_ind]], [hor_median_ind, hor_median_ind], 'r-')
    # plt.subplot(1, 3, 3)
    # plt.imshow(comp, cmap='bone')
    # plt.plot(np.arange(0, image.shape[1]), first_nonzeros_vert, 'g.')
    # plt.plot(np.arange(0, image.shape[1]), last_nonzeros_vert, 'g.')
    # plt.plot([vert_max_ind, vert_max_ind], [first_nonzeros_vert[vert_max_ind], last_nonzeros_vert[vert_max_ind]], 'g-')
    # plt.suptitle('Ratio: ' + str(ratio))
    # plt.show()

    return ratio

def first_nonzero(arr, axis, invalid_val=-1):
    """Placeholder."""
    mask = (arr!=0)
    return np.where(mask.any(axis=axis), mask.argmax(axis=axis), invalid_val)

def last_nonzero(arr, axis, invalid_val=-1):
    """Placeholder."""
    mask = (arr!=0)
    val = arr.shape[axis] - np.flip(mask, axis=axis).argmax(axis=axis) - 1
    return np.where(mask.any(axis=axis), val, invalid_val)

def getBiggestComp(image):
    """ Uses connected components to get the breast """
    structure = np.ones([3,3], dtype=np.int) # Relational matrix (8-connected)
    # Run connected components to label the various connected components
    labeled_image, n_components = label(image, structure=structure) 

    counts = np.bincount(labeled_image.flatten())
    ind = np.argmax(counts[1:]) + 1
    biggestComp = (labeled_image == ind).astype(np.uint8)

    return biggestComp

def calc_image_prof(image):
    """Placeholder."""
    image_square = cv2.resize(image, (200, 200), interpolation=cv2.INTER_AREA)
    
    hor_profile = np.mean(image_square, axis=0)
    vert_profile = np.mean(image_square, axis=1)

    # plt.subplot(1, 2, 1)
    # plt.imshow(image_square, cmap='bone')
    # plt.subplot(1, 2, 2)
    # plt.plot(np.arange(0, 200), hor_profile, label='Horizontal')
    # plt.plot(np.arange(0, 200), vert_profile, label='Vertical')
    # plt.legend()
    # plt.show()

    return hor_profile, vert_profile

def preprocessing(image, record):
    """Placholder."""
    highest_possible_intensity = (np.power(2, record['bits_stored']) - 1)
    image_norm = image/highest_possible_intensity

    # These images aren't in Hounsfield units and are most likely already windowed (VOI LUT)
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
    
    return image_downsize

def contrast_stretch(image, min_I, max_I):
    """Placeholder."""
    # All values < min_I will be 0 and all values > max_I will be 1
    image_copy = image.copy()

    try: 
        A = np.array([[min_I, 1], [max_I, 1]])
        B = [0, 1]

        [slope, intercept] = np.linalg.solve(A, B)

        image_copy[np.where((image_copy >= min_I) & (image_copy <= max_I))] = \
            slope * image_copy[np.where((image_copy >= min_I) & (image_copy <= max_I))] + intercept

        image_copy[np.where(image < min_I)] = 0
        image_copy[np.where(image > max_I)] = 1
    except np.linalg.LinAlgError as err:
        if 'Singular matrix' in str(err):
            print('SINGULAR MATRIX: NOT DOING CONTRAST STRETCH')
        else:
            raise

    return image_copy
