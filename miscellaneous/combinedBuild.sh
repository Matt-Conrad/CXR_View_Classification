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

virtualenv -p /usr/bin/python3.6 CXR_env
source CXR_env/bin/activate

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
export LD_LIBRARY_PATH="./CXR_env/lib/python3.6/site-packages/PyQt5/Qt/lib:$PATH" #Replace period with explicit file location

mkdir ../Combined/DesktopApp/build
cd ../Combined/DesktopApp/build

if [ "$1" == "g++" ]
then
    cp -r ../src/* .

    g++ -std=c++17 -c -fPIC confighandler.cpp -o confighandler.o
    g++ -std=c++17 -c -fPIC databasehandler.cpp -o databasehandler.o
    g++ -std=c++17 -c -fPIC -I/opt/qt515/include downloader.cpp -o downloader.o
    g++ -std=c++17 -c -fPIC unpacker.cpp -o unpacker.o
    g++ -std=c++17 -c -fPIC storer.cpp -o storer.o
    g++ -std=c++17 -c -fPIC -I/usr/include/opencv4 -I/opt/qt515/include featurecalculator.cpp -o featurecalculator.o
    g++ -std=c++17 -c -fPIC labelimporter.cpp -o labelimporter.o
    g++ -std=c++17 -c -fPIC -fopenmp -I/opt/qt515/include trainer.cpp -o trainer.o

    g++ -shared -Wl,-soname,libdownloader.so -Wl,-rpath=/opt/qt515/lib -L/opt/qt515/lib -o libdownloader.so downloader.o -lQt5Network confighandler.o -lboost_system -lstdc++fs 
    g++ -shared -Wl,-soname,libunpacker.so -o libunpacker.so unpacker.o -lz -lbz2 -larchive confighandler.o -lboost_system -lstdc++fs
    g++ -shared -Wl,-soname,libstorer.so -o libstorer.so storer.o -ldcmimgle -ldcmdata databasehandler.o -lpqxx -lpq confighandler.o -lboost_system -lstdc++fs
    g++ -shared -Wl,-soname,libfeaturecalculator.so -Wl,-rpath=/opt/qt515/lib -L/opt/qt515/lib -o libfeaturecalculator.so featurecalculator.o -lQt5Core -ldcmimgle -ldcmdata -lopencv_core -lopencv_imgproc databasehandler.o -lpqxx -lpq confighandler.o -lboost_system -lstdc++fs
    g++ -shared -Wl,-soname,liblabelimporter.so -o liblabelimporter.so labelimporter.o databasehandler.o -lpqxx -lpq confighandler.o -lboost_system -lstdc++fs
    g++ -shared -Wl,-soname,libtrainer.so -Wl,-rpath=/opt/qt515/lib -L/opt/qt515/lib -o libtrainer.so trainer.o -lQt5Core databasehandler.o -lpqxx -lpq -larmadillo -lmlpack confighandler.o -lboost_system -lstdc++fs
elif [ "$1" == "make" ]
then
    cp ../src/Makefile ./Makefile
    make
elif [ "$1" == "cmake" ]
then
    cmake ../src
    cmake --build .
else
    echo "MUST PROVIDE BUILD PARAMETER"
fi