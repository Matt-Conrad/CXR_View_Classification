"""This script is used to send a random test DCM file to a server"""
import os
import logging
import csv
import random
import time
from datetime import datetime
import pydicom as pdm
import matplotlib.pyplot as plt
import requests
import sys

# url = "http://" + sys.argv[1] + "/api/classify" # Send to a separate machine on network
url = "http://localhost:5000/api/classify"

# Randomize folder to be chosen from
with open('test_images.csv', newline='') as f:
    reader = csv.reader(f)
    test_images = list(reader)
    random.shuffle(test_images)

for test_image in test_images:
    file_name = test_image[0]
    folder = file_name.split("_")[0]
    full_path = "../datasets/NLMCXR_dcm/" + folder + "/" + file_name

    if not os.path.exists(full_path):
        logging.debug("%s does not exist", file_name)
        continue
   
    # Display the image
    dcm = pdm.dcmread(full_path)
    image = dcm.pixel_array

    # Read as binary
    with open(full_path, "rb") as image_file:
        dcmBinary = image_file.read()

    # Send binary data over HTTP
    print(str(datetime.now()) + " Sending " + file_name)
    send_headers = {"Content-Type": "application/octet-stream"}
    response = requests.post(url, data=dcmBinary, headers=send_headers)
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