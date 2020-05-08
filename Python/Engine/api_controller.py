"""Contains the code that controls the web interfaces."""
import os
from flask import Flask, render_template, abort, jsonify, request
from joblib import load
import pydicom as pdm
import numpy as np
from shared_image_processing.features import calc_image_prof
from cxr_pipeline.preprocessing import preprocessing

app = Flask(__name__)

@app.route('/')
def how_to():
    return render_template('how_to_page.html')

@app.route("/api/classify", methods=["POST"])
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
    image = preprocessing(dcm.pixel_array, dcm['BitsStored'].value, dcm['PhotometricInterpretation'].value)

    # Calculate the features
    (hor_profile, vert_profile) = calc_image_prof(image)

    # Feed feature vector to loaded classifier from the training app
    full_profile = np.concatenate((hor_profile, vert_profile))
    full_profile = np.reshape(full_profile, (400, 1))
    full_profile = np.transpose(full_profile)

    clf = load("full_set_classifier.joblib")

    result = clf.predict(full_profile)[0]

    return jsonify({'result': result}), 200

if __name__ == "__main__":
    # app.run() # Show to only localhost
    app.run(host='0.0.0.0') # Show to other computers on network