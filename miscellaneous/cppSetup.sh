#!/bin/bash
sudo apt-get update

if [ "$1" == "prebuilt" ]
then
    sudo apt-get install libpqxx-6.4 dcmtk libopencv-core4.2 libopencv-imgproc4.2 libmlpack3 qt5-default -y
elif [ "$1" == "build" ]
then
    sudo apt-get install g++ make libpqxx-dev libdcmtk-dev libopencv-dev libmlpack-dev qt5-default libspdlog-dev libarchive-dev libensmallen-dev libbz2-dev libboost-dev libboost-system-dev -y
fi
