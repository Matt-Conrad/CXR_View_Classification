"""This script is used to send a random DCM file to the Flask Dev server on the local machine."""
import os
import logging
import csv
import pydicom as pdm
import matplotlib.pyplot as plt
import requests

# Randomize folder to be chosen from
with open('test_images.csv', newline='') as f:
    reader = csv.reader(f)
    test_images = list(reader)

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
    url = "http://127.0.0.1:80/api/classify"
    send_headers = {"Content-Type": "application/octet-stream"}
    response = requests.post(url, data=encoded_string_bin, headers=send_headers)

    if response.status_code == 200:
        plt.imshow(image, cmap="bone")
        plt.title(file_name + " classified as: " + response.json()["result"])
        plt.show()