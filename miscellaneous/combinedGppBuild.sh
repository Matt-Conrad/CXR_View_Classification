#!/bin/bash
# Starting at the DesktopApp directory, enter the following commands in the Linux command prompt to build 
# the shared libraries using g++ and the command line:

g++ -std=c++17 -c -fPIC confighandler.cpp -o confighandler.o
g++ -std=c++17 -c -fPIC databasehandler.cpp -o databasehandler.o
g++ -std=c++17 -c -fPIC -I/home/matthew/Qt5/5.15.1/gcc_64/include -I/home/matthew/Qt5/5.15.1/gcc_64/include/QtNetwork -I/home/matthew/Qt5/5.15.1/gcc_64/include/QtCore downloader.cpp -o downloader.o 
g++ -std=c++17 -c -fPIC unpacker.cpp -o unpacker.o
g++ -std=c++17 -c -fPIC storer.cpp -o storer.o
g++ -std=c++17 -c -fPIC -I/usr/local/include/opencv4 featurecalculator.cpp -o featurecalculator.o
g++ -std=c++17 -c -fPIC labelimporter.cpp -o labelimporter.o
g++ -std=c++17 -c -fPIC trainer.cpp -o trainer.o

g++ -shared -Wl,-soname,libdownloader.so -Wl,-rpath,/home/matthew/Qt5/5.15.1/gcc_64/lib -o libdownloader.so downloader.o -lQt5Network -lQt5Core confighandler.o -lboost_system -lstdc++fs 
g++ -shared -Wl,-soname,libunpacker.so -o libunpacker.so unpacker.o -lz -lbz2 -larchive confighandler.o -lboost_system -lstdc++fs
g++ -shared -Wl,-soname,libstorer.so -o libstorer.so storer.o -ldcmimgle -ldcmdata databasehandler.o -lpqxx -lpq confighandler.o -lboost_system -lstdc++fs
g++ -shared -Wl,-soname,libfeaturecalculator.so -o libfeaturecalculator.so featurecalculator.o -ldcmimgle -ldcmdata -lopencv_core -lopencv_imgproc databasehandler.o -lpqxx -lpq confighandler.o -lboost_system -lstdc++fs
g++ -shared -Wl,-soname,liblabelimporter.so -o liblabelimporter.so labelimporter.o databasehandler.o -lpqxx -lpq confighandler.o -lboost_system -lstdc++fs
g++ -shared -Wl,-soname,libtrainer.so -o libtrainer.so trainer.o databasehandler.o -lpqxx -lpq -fopenmp -larmadillo -lmlpack confighandler.o -lboost_system -lstdc++fs