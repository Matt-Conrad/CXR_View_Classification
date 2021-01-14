#!/bin/bash
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt-get update

if [ "$1" == "source" ] || [ "$1" == "engine" ]
then
    sudo apt-get install python3.6 -y
elif [ "$1" == "build" ]
then
    sudo apt-get install python3.6-dev gcc -y
fi

sudo apt-get install python3-virtualenv -y
sudo apt-get install libxcb-xinerama0 -y # If running at all I think

virtualenv -p /usr/bin/python3.6 CXR_env
sudo chmod -R a+rwx CXR_env #maybe remove

source CXR_env/bin/activate

if [ "$1" == "source" ] || [ "$1" == "build" ]
then
    # cd /mnt/hgfs/SharedFolder_Guest/miscellaneous # For CI/CD, otherwise comment out and run from misc folder
    pip install -r requirements.txt
elif [ "$1" == "engine" ]
then
    # cd /mnt/hgfs/SharedFolder_Guest/miscellaneous # For CI/CD, otherwise comment out and run from misc folder
    pip install -r engineRequirements.txt
fi