#!/bin/bash
sudo add-apt-repository ppa:deadsnakes/ppa -y

if [ "$1" != "download" ] 
then
    sudo add-apt-repository ppa:beineri/opt-qt-5.15.2-focal -y
fi

sudo apt-get update
sudo apt-get install python3.6 python3-virtualenv -y

if [ "$1" == "download" ] 
then
    sudo apt-get install libxcb-xinerama0 -y
fi

virtualenv -p /usr/bin/python3.6 $HOME/CXR_env
source $HOME/CXR_env/bin/activate

cd /mnt/hgfs/SharedFolder_Guest/miscellaneous
pip install -r requirements.txt

if [ "$1" == "download" ]
then
    sudo apt-get install dcmtk libopencv-core4.2 libopencv-imgproc4.2 libmlpack3 libpqxx-6.4 -y
fi

if [ "$1" != "download" ]
then
    sudo apt-get install g++ libboost-dev libboost-system-dev libpqxx-dev libarchive-dev libdcmtk-dev libopencv-dev libmlpack-dev libensmallen-dev libbz2-dev qt515base -y
fi

if [ "$1" == "make" ]
then
    sudo apt-get install make -y
elif [ "$1" == "cmake" ]
then
    sudo apt-get install cmake -y
fi

# TO LINK QT FROM PYQT5 - must run this in terminal before running main.py when doing the download option
export LD_LIBRARY_PATH="$HOME/CXR_env/lib/python3.6/site-packages/PyQt5/Qt/lib:$PATH"