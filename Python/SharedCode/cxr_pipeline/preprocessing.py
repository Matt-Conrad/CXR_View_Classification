import logging
import numpy as np
import cv2
from shared_image_processing.enhancement import contrast_stretch

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