"""This script is used to send a random DCM file to the Flask Dev server on the local machine."""
import os
from random import randint
import base64
import pydicom as pdm
import matplotlib.pyplot as plt
import requests

# Randomize folder to be chosen from
folder = randint(1, 3999)
folder_path = "./NLMCXR_dcm/" + str(folder) + "/"

# Randomize the file in the folder to use
image_names = os.listdir(folder_path)
file_ind = randint(0, len(image_names)-1)
file_name = image_names[file_ind]

full_path = folder_path + file_name
print("Chosen file: " + full_path)

# Display the image
dcm = pdm.dcmread(full_path)
image = dcm.pixel_array
plt.imshow(image, cmap="bone")
plt.show()

# Convert DCM file as follows: binary => b64 => ASCII
with open(full_path, "rb") as image_file:
    encoded_string_bin = image_file.read()
    encoded_string_b64 = base64.b64encode(encoded_string_bin)
encoded_string_ascii = encoded_string_b64.decode("ascii")

# Send ASCII version of file in a JSON over HTTP
url = "http://127.0.0.1:5000/api/classify"
send_headers = {"Content-Type": "application/json"}
response = requests.post(url, json={"dicom_data": encoded_string_ascii}, headers=send_headers)

print("Classification: " + response.json()["result"])