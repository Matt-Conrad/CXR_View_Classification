#!/bin/bash
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt-get update
sudo apt-get install python3.6 -y
sudo apt-get install python3.6-dev -y
sudo apt-get install python3-dev -y
sudo apt-get install gcc -y
sudo apt-get install python3-virtualenv -y
sudo apt-get install libxcb-xinerama0 -y
# TODO: Thin out the list above. Probably some of them are not needed. 
# NOTE: libxcb-xinerama0 is due to an error message from Qt

virtualenv -p /usr/bin/python3.6 CXR_env
sudo chmod -R a+rwx CXR_env #maybe remove

source CXR_env/bin/activate

cd /mnt/hgfs/SharedFolder_Guest/miscellaneous
pip install -r /mnt/hgfs/SharedFolder_Guest/miscellaneous/requirements.txt