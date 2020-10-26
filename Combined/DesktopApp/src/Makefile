CXX = g++
CXXFLAGS = -std=c++17 -fPIC -c
SHAREDFLAGS = -shared

all: confighandler.o databasehandler.o downloader.o unpacker.o storer.o featurecalculator.o labelimporter.o trainer.o \
	libdownloader.so libunpacker.so libstorer.so libfeatcalc.so liblabelimporter.so libtrainer.so

confighandler.o: confighandler.h
	$(CXX) $(CXXFLAGS) confighandler.cpp -o confighandler.o

databasehandler.o: databasehandler.h
	$(CXX) $(CXXFLAGS) databasehandler.cpp -o databasehandler.o

downloader.o: downloader.h
	$(CXX) $(CXXFLAGS) -I/home/matthew/Qt5/5.15.1/gcc_64/include -I/home/matthew/Qt5/5.15.1/gcc_64/include/QtNetwork -I/home/matthew/Qt5/5.15.1/gcc_64/include/QtCore downloader.cpp -o downloader.o

unpacker.o: unpacker.h
	$(CXX) $(CXXFLAGS) unpacker.cpp -o unpacker.o

storer.o: storer.h
	$(CXX) $(CXXFLAGS) storer.cpp -o storer.o

featurecalculator.o: featurecalculator.h
	$(CXX) $(CXXFLAGS) -I/usr/local/include/opencv4 featurecalculator.cpp -o featurecalculator.o

labelimporter.o: labelimporter.h
	$(CXX) $(CXXFLAGS) labelimporter.cpp -o labelimporter.o

trainer.o: trainer.h
	$(CXX) $(CXXFLAGS) trainer.cpp -o trainer.o


libdownloader.so: downloader.o confighandler.o
	$(CXX) $(SHAREDFLAGS) -Wl,-soname,libdownloader.so -Wl,-rpath,/home/matthew/Qt5/5.15.1/gcc_64/lib -o libdownloader.so downloader.o -lQt5Network -lQt5Core confighandler.o -lboost_system -lstdc++fs 

libunpacker.so: unpacker.o confighandler.o
	$(CXX) $(SHAREDFLAGS) -Wl,-soname,libunpacker.so -o libunpacker.so unpacker.o -lz -lbz2 -larchive confighandler.o -lboost_system -lstdc++fs

libstorer.so: storer.o confighandler.o databasehandler.o
	$(CXX) $(SHAREDFLAGS) -Wl,-soname,libstorer.so -o libstorer.so storer.o -ldcmimgle -ldcmdata databasehandler.o -lpqxx -lpq confighandler.o -lboost_system -lstdc++fs

libfeatcalc.so: featurecalculator.o confighandler.o databasehandler.o
	$(CXX) $(SHAREDFLAGS) -Wl,-soname,libfeatcalc.so -o libfeatcalc.so featurecalculator.o -ldcmimgle -ldcmdata -lopencv_core -lopencv_imgproc databasehandler.o -lpqxx -lpq confighandler.o -lboost_system -lstdc++fs

liblabelimporter.so: labelimporter.o confighandler.o databasehandler.o
	$(CXX) $(SHAREDFLAGS) -Wl,-soname,liblabelimporter.so -o liblabelimporter.so labelimporter.o databasehandler.o -lpqxx -lpq confighandler.o -lboost_system -lstdc++fs

libtrainer.so: trainer.o confighandler.o databasehandler.o
	$(CXX) $(SHAREDFLAGS) -Wl,-soname,libtrainer.so -o libtrainer.so trainer.o databasehandler.o -lpqxx -lpq -fopenmp -larmadillo -lmlpack confighandler.o -lboost_system -lstdc++fs
