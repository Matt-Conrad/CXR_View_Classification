#!/bin/bash
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt-get update
sudo apt-get install python3.6 -y
sudo apt-get install python3-virtualenv -y
sudo apt-get install libxcb-xinerama0 -y

virtualenv -p /usr/bin/python3.6 $HOME/CXR_env

source $HOME/CXR_env/bin/activate

cd /mnt/hgfs/SharedFolder_Guest/miscellaneous
pip install -r requirements.txt

sudo apt-get install dcmtk -y
sudo apt-get install libopencv-core4.2 libopencv-imgproc4.2 -y
sudo apt-get install libmlpack3 -y
sudo apt-get install libpqxx-6.4 -y

# TO LINK QT FROM PYQT5 - must run this in terminal before running main.py
export LD_LIBRARY_PATH="$HOME/CXR_env/lib/python3.6/site-packages/PyQt5/Qt/lib:$PATH"
