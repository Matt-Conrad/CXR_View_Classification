"""Contains function that implements 'Orientation Correction for Chest Images'."""
import logging
import os
# import time
import numpy as np
import pydicom as pdm
import psycopg2
import psycopg2.extras
# import matplotlib.pyplot as plt
import cv2
# from scipy.ndimage.measurements import label
from skimage.feature import hog
from metadata_to_db.config import config
from shared_image_processing.connectedComponents import getBiggestComp
from shared_image_processing.enhancement import contrast_stretch
from shared_image_processing.features import calc_image_prof

def calculate_features(config_file_name):
    """Cycles through the table and pulls one image at a time.
    
    Parameters
    ----------
    config_file_name : string
        The INI file with DB and folder configuration information
    """
    logging.info('Calculating features from images')
    conn = None
    try:
        # read the connection parameters
        params = config(filename=config_file_name, section='postgresql')
        table_name = config(filename=config_file_name, section='table_info')['metadata_table_name']
        # connect to the PostgreSQL server
        logging.debug('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        logging.debug('Connection established')
        # Create the SQL query to be used
        sql_query = 'SELECT * FROM ' + table_name + ';'
        # create table one by one
        cur.execute(sql_query)
        count = 0
        for record in cur:
            # Read the image data
            file_path = record['file_path']
            count += 1
            logging.info('Calculating for image number: %s File: %s', str(count), file_path)
            image = pdm.dcmread(file_path).pixel_array
            
            # Preprocess the image
            image = preprocessing(image, record)

            # Calculate the various features
            (hor_profile, vert_profile) = calc_image_prof(image)
            
            ratio = calc_body_size_ratio(image)
            
            phog_vector = phog(image, n_bins=8, orient_range=(0, 360), levels=3)

            # Store the data to the DB
            store(config_file_name, file_path, ratio, hor_profile, vert_profile, phog_vector)

        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (psycopg2.DatabaseError) as error:
        logging.warning(error)
    finally:
        if conn is not None:
            conn.close()
            logging.info('Done calculating features from images')

def store(config_file_name, file_path, ratio, hor_profile, vert_profile, pyr_hog):
    """Stores the calculated features into the database.
    
    Parameters
    ----------
    config_file_name : string
        The INI file with DB and folder configuration information
    file_path : string
        Path to the image file
    ratio : float
        Ratio of torso dimensions
    hor_profile : float[]
        Vector containing horizontal profile of torso
    vert_profile : float[]
        Vector containing vertical profile of torso
    pyr_hog : float[]
        Vector containing the pyramid HOG
    """
    logging.debug('Storing the calculated features into the database.')
    conn = None
    try:
        # read the connection parameters
        params = config(filename=config_file_name, section='postgresql')
        out_table_name = config(filename=config_file_name, section='table_info')['features_table_name']
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # Create the SQL query to be used
        sql_query = 'INSERT INTO ' + out_table_name + ' (file_name, file_path, body_size_ratio, hor_profile, vert_profile, phog) VALUES (%s, %s, %s, %s, %s, %s);'
        values = (file_path.split(os.sep)[-1], file_path, ratio, hor_profile.tolist(), vert_profile.tolist(), pyr_hog.tolist())
        # create table one by one
        cur.execute(sql_query, values)

        cur.close()
        # commit the changes
        conn.commit()
    except (psycopg2.DatabaseError) as error:
        logging.warning(error)
    finally:
        if conn is not None:
            conn.close()
            logging.debug('Done storing.')

def phog(image, n_bins, orient_range, levels):
    """Calculates the pyramid histogram of oriented gradients.
    
    Parameters
    ----------
    image : ndarray
        Image data
    n_bins : int
        Number of bins to use for each cell
    orient_range : tuple?
        Range of orientations
    levels : int
        Number of levels in the pyramid
    
    Returns
    -------
    float[]
        The full PHOG vector
    """
    # Going with this for now. If this doesn't work for some reason, try the cv2 one or try the
    # imlementation of it at:
    # https://github.com/ReseachWithDrSun/test/blob/fdae985309e488de42b7ac3c88306345b2d739e7/dtyu/xray_learning/phog_features/phog.py

    # NOTE: might need to include some form of Canny edge detector in here somewhere
    logging.debug('Calculating the phog of the image')

    # Use skimage's hog at at different levels
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
    
    # Visualize
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

    logging.debug('Done calculating the phog.')

    return np.concatenate((feature_vector0, feature_vector1, feature_vector2, feature_vector3))

def calc_body_size_ratio(image):
    """Calculates the body size ratio.
    
    Parameters
    ----------
    image : ndarray
        Image data
    
    Returns
    -------
    float
        The body size ratio
    """
    logging.debug('Calculating the body size ratio')

    # Threshold the image at the median intensity
    median = np.median(image)
    image_binarized = (image >= median).astype(np.uint8)

    # Get the biggest component of the threshold image
    comp = getBiggestComp(image_binarized)

    # Get the first and last non-zero pixels along each horizontal
    first_nonzeros_hor = first_nonzero(comp, axis=1, invalid_val=np.nan)
    last_nonzeros_hor = last_nonzero(comp, axis=1, invalid_val=np.nan)

    # Get the first and last non-zero pixels along each vertical
    first_nonzeros_vert = first_nonzero(comp, axis=0, invalid_val=np.nan)
    last_nonzeros_vert = last_nonzero(comp, axis=0, invalid_val=np.nan)

    # Find the length of each cross-section
    hor_cross_sections = last_nonzeros_hor - first_nonzeros_hor
    vert_cross_sections = last_nonzeros_vert - first_nonzeros_vert

    # Find median horizontal cross-section length and maximum vertical cross-section length & their indices
    hor_median = np.nanmedian(hor_cross_sections)
    vert_max = np.nanmax(vert_cross_sections)
    vert_max_ind = np.nanargmax(vert_cross_sections)
    hor_median_ind = np.argsort(hor_cross_sections)[len(hor_cross_sections)//2]

    # Take the ratio
    ratio = hor_median/vert_max

    # Visualize
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

    logging.debug('Done calculating the body size ratio')

    return ratio

def first_nonzero(arr, axis, invalid_val=-1):
    """Get the first non-zero pixels along a dimension
    
    Parameters
    ----------
    arr : ndarray
        2D array
    axis : int
        The axis to go along
    invalid_val : int, optional
        Value to use, by default -1
    
    Returns
    -------
    float[]
        1D-array with all the first non-zero pixel indices
    """
    mask = (arr!=0)
    return np.where(mask.any(axis=axis), mask.argmax(axis=axis), invalid_val)

def last_nonzero(arr, axis, invalid_val=-1):
    """Get the last non-zero pixels along a dimension
    
    Parameters
    ----------
    arr : ndarray
        2D array
    axis : int
        The axis to go along
    invalid_val : int, optional
        Value to use, by default -1
    
    Returns
    -------
    float[]
        1D-array with all the last non-zero pixel indices
    """
    mask = (arr!=0)
    val = arr.shape[axis] - np.flip(mask, axis=axis).argmax(axis=axis) - 1
    return np.where(mask.any(axis=axis), val, invalid_val)

def preprocessing(image, record):
    """Runs the preprocessing steps on the image.
    
    Parameters
    ----------
    image : ndarray
        Image data
    record : psycopg2 record object?
        The metadata record for the image
    
    Returns
    -------
    ndarray
        Preprocessed image
    
    Raises
    ------
    ValueError
        Raise error if image is not MONOCHROME1 or MONOCHROME2 as expected
    """
    logging.debug('Beginning preprocessing on %s', record['file_path'])

    # Normalize image
    highest_possible_intensity = (np.power(2, record['bits_stored']) - 1)
    image_norm = image/highest_possible_intensity

    # These images aren't in Hounsfield units and are most likely already windowed (VOI LUT)
    # window_center = record['window_center']/highest_possible_intensity
    # window_width = record['window_width']/highest_possible_intensity
    # min_I = window_center - (window_width/2)
    # max_I = window_center + (window_width/2)

    # Apply contrast stretch transform
    # image_norm = contrast_stretch(image_norm, min_I, max_I)

    # Invert the image if it's MONOCHROME1
    if record['photometric_interpretation'] == 'MONOCHROME1':
        image_norm = 1 - image_norm
    elif record['photometric_interpretation'] == 'MONOCHROME2':
        pass
    else:
        raise ValueError('Image is not MONOCHROME1 or MONOCHROME2 as expected.')

    # Find the percentile intensities
    saturation_vals = np.percentile(image_norm.flatten(), [1, 99])

    # Contrast stretch the image using the percentiles
    image_enhanced = contrast_stretch(image_norm, saturation_vals[0], saturation_vals[1])

    # Threshold the image at the median intensity
    median = np.median(image_enhanced)
    image_binarized = (image_enhanced >= median).astype(np.uint8)

    # get the bounding rect
    x, y, w, h = cv2.boundingRect(image_binarized)

    # draw a green rectangle to visualize the bounding rect
    image_enh_copy = image_enhanced.copy()
    cv2.rectangle(image_enh_copy, (x, y), (x+w, y+h), 1, 2)

    # Crop the image
    image_cropped = image_enhanced[y:y+h, x:x+w]

    # Downscale the image
    scale_percent = .5
    width = int(image_cropped.shape[1] * scale_percent)
    height = int(image_cropped.shape[0] * scale_percent)
    dim = (width, height)
    image_downsize = cv2.resize(image_cropped, dim, interpolation=cv2.INTER_AREA)

    logging.debug('Preprocessing completed.')
    
    return image_downsize
