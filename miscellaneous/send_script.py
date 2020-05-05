"""This script is used to send a random DCM file to the Flask Dev server on the local machine."""
import os
import logging
import csv
import pydicom as pdm
import matplotlib.pyplot as plt
import numpy as np
import random
import requests
import time
from datetime import datetime

# Randomize folder to be chosen from
with open('test_images.csv', newline='') as f:
    reader = csv.reader(f)
    test_images = list(reader)
    random.shuffle(test_images)

for test_image in test_images:
    file_name = test_image[0]
    folder = file_name.split("_")[0]
    full_path = "./NLMCXR_dcm/" + folder + "/" + file_name

    if not os.path.exists(full_path):
        logging.debug("%s does not exist", file_name)
        continue
   
    # Display the image
    dcm = pdm.dcmread(full_path)
    image = dcm.pixel_array

    # Convert DCM file as follows: binary => b64 => ASCII
    with open(full_path, "rb") as image_file:
        encoded_string_bin = image_file.read()

    # Send ASCII version of file in a JSON over HTTP
    print(str(datetime.now()) + " Sending " + file_name)
    # url = "http://**ELASTIC_BEANSTALK_INSTANCE_URL**/api/classify" # Send to AWS service
    url = "http://127.0.0.1:5000/api/classify" # Send to local service
    send_headers = {"Content-Type": "application/octet-stream"}
    response = requests.post(url, data=encoded_string_bin, headers=send_headers)
    print(str(datetime.now()) + " Received " + file_name)
    if response.status_code == 200:
        plt.imshow(image, cmap="bone")
        plt.title(file_name + " classified as: " + response.json()["result"])
        plt.show()
    else:
        print(str(datetime.now()) + " Response code: " + str(response.status_code))
        print(str(datetime.now()) + " Response headers: " + str(response.headers))
        print(str(datetime.now()) + " Response body: " + str(response.content))
    time.sleep(5)