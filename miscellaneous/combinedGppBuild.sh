#!/bin/bash
mkdir Combined/DesktopApp/build
cd Combined/DesktopApp/build
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
