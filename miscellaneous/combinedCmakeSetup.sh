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

virtualenv -p /usr/bin/python3.6 $HOME/CXR_env

source $HOME/CXR_env/bin/activate

cd /mnt/hgfs/SharedFolder_Guest/miscellaneous
pip install -r /mnt/hgfs/SharedFolder_Guest/miscellaneous/requirements.txt

sudo apt-get update
sudo apt-get install g++ -y
sudo apt-get install cmake -y
sudo apt-get install libpqxx-dev -y
sudo apt-get install libdcmtk-dev -y
sudo apt-get install libopencv-dev -y
sudo apt-get install libmlpack-dev -y
sudo apt-get install libarchive-dev -y
sudo apt-get install libensmallen-dev -y
sudo apt-get install libbz2-dev -y
sudo apt-get install libboost-all-dev -y

sudo add-apt-repository ppa:beineri/opt-qt-5.15.2-focal -y
sudo apt-get update
sudo apt install qt515base -y