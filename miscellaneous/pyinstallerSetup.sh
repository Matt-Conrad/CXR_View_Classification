#!/bin/bash
add-apt-repository ppa:deadsnakes/ppa -y
apt-get update
apt-get install python3.6 -y
apt-get install python3.6-dev -y
apt-get install python3-dev -y
apt-get install gcc -y
apt-get install python3-virtualenv -y
apt-get install libxcb-xinerama0 -y
# TODO: Thin out the list above. Probably some of them are not needed. 
# NOTE: libxcb-xinerama0 is due to an error message from Qt

virtualenv -p /usr/bin/python3.6 CXR_env
sudo chmod -R a+rwx CXR_env #maybe remove

source CXR_env/bin/activate

pip install -r ./requirements.txt