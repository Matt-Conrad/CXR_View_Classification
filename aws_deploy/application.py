"""Contains the code that controls the web interfaces."""
import os
import logging
from flask import Flask, render_template, abort, jsonify, request
from joblib import load
import pydicom as pdm
import numpy as np
import cv2

application = Flask(__name__)

@application.route('/')
def how_to():
    return render_template('how_to_page.html')

@application.route("/api/classify", methods=["POST"])
def classify():
    # Deny requests that we don't care about
    if not request.data:
        abort(400, "No data provided")
    
    if "Content-Type" not in request.headers:
        abort(400, "No content-type header")
    
    if request.headers["Content-Type"] != "application/octet-stream":
        abort(400, "Content-Type is not application/octet-stream")

    # Save the binary as a DCM file, read it into a pydicom object, delete DCM file
    temp_file = "./temp.dcm"

    with open(temp_file, "wb") as out_file:
        out_file.write(request.data)

    dcm = pdm.dcmread(temp_file)
    os.remove(temp_file)

    # Preprocess image
    image = preprocessing(dcm)

    # Calculate the features
    (hor_profile, vert_profile) = calc_image_prof(image)

    # Feed feature vector to loaded classifier from the training app
    full_profile = np.concatenate((hor_profile, vert_profile))
    full_profile = np.reshape(full_profile, (400, 1))
    full_profile = np.transpose(full_profile)

    clf = load("full_set_classifier.joblib")
    result = clf.predict(full_profile)[0]

    return jsonify({'result': result}), 200


def preprocessing(dcm_image):
    """Runs the preprocessing steps on the image.

    NOTE: This function is from the calculate_features.py file and is only here temporarily
    
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
    image = dcm_image.pixel_array

    # Normalize image
    highest_possible_intensity = (np.power(2, dcm_image['BitsStored'].value) - 1)
    image_norm = image/highest_possible_intensity

    # These images aren't in Hounsfield units and are most likely already windowed (VOI LUT)
    # window_center = record['window_center']/highest_possible_intensity
    # window_width = record['window_width']/highest_possible_intensity
    # min_I = window_center - (window_width/2)
    # max_I = window_center + (window_width/2)

    # Apply contrast stretch transform
    # image_norm = contrast_stretch(image_norm, min_I, max_I)

    # Invert the image if it's MONOCHROME1
    if dcm_image['PhotometricInterpretation'].value == 'MONOCHROME1':
        image_norm = 1 - image_norm
    elif dcm_image['PhotometricInterpretation'].value == 'MONOCHROME2':
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

def calc_image_prof(image):
    """Calculate the mean horizontal and vertical profiles.
    
    Parameters
    ----------
    image : ndarray
        Image data
    
    Returns
    -------
    (float[], float[])
        The mean horizontal and vertical profiles
    """
    logging.debug('Calculating the profiles of the image')
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

    logging.debug('Done calculating the profiles of the image')

    return hor_profile, vert_profile

def contrast_stretch(image, min_I, max_I):
    """Apply the contrast stretch transformation to the image.

    All values < min_I will be 0 and all values > max_I will be 1.
    
    Parameters
    ----------
    image : ndarray
        Image data
    min_I : int
        Intensity floor
    max_I : int
        Intensity ceiling
    
    Returns
    -------
    ndarray
        Contrast-stretch image
    """
    # copy image
    image_copy = image.copy()

    try: 
        # Apply transform
        A = np.array([[min_I, 1], [max_I, 1]])
        B = [0, 1]

        [slope, intercept] = np.linalg.solve(A, B)

        image_copy[np.where((image_copy >= min_I) & (image_copy <= max_I))] = \
            slope * image_copy[np.where((image_copy >= min_I) & (image_copy <= max_I))] + intercept

        image_copy[np.where(image < min_I)] = 0
        image_copy[np.where(image > max_I)] = 1
    except np.linalg.LinAlgError as err:
        # Ignore singular matrix issues and raise other issues
        if 'Singular matrix' in str(err):
            logging.warning('SINGULAR MATRIX: NOT DOING CONTRAST STRETCH')
        else:
            raise

    return image_copy

if __name__ == "__main__":
    application.run()