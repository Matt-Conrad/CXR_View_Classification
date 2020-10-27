CXX = g++
CXXFLAGS = -std=c++17 -fPIC -c
SHAREDFLAGS = -shared -Wl,-soname,$@ -Wl,-rpath,/home/matthew/Qt5/5.15.1/gcc_64/lib

SRCS := confighandler.cpp \
    databasehandler.cpp \
	downloader.cpp \
	unpacker.cpp \
	storer.cpp \
	featurecalculator.cpp \
	labelimporter.cpp \
	trainer.cpp


SHARED_OBJS1 = libdownloader.so \
	libunpacker.so

SHARED_OBJS2 = libstorer.so \
	libfeatcalc.so \
	liblabelimporter.so \
	libtrainer.so

OBJS := ${SRCS:cpp=o} 
HEADERS := ${SRCS:cpp=h} 
NAMES := ${SRCS:.cpp=} 

LIBS = -lQt5Network -lQt5Core -lopencv_core -lopencv_imgproc -lz -lbz2 -larchive -ldcmimgle -ldcmdata -lpqxx -lpq -fopenmp -larmadillo -lmlpack -lboost_system -lstdc++fs 

INCPATH = -I/home/matthew/Qt5/5.15.1/gcc_64/include -I/home/matthew/Qt5/5.15.1/gcc_64/include/QtNetwork -I/home/matthew/Qt5/5.15.1/gcc_64/include/QtCore 
INCPATH += -I/usr/local/include/opencv4

.PHONY: all clean

all: ${OBJS} ${SHARED_OBJS1} ${SHARED_OBJS2}

clean :
	rm -f *.o *.so

$(OBJS): %.o : %.cpp %.h
	$(CXX) $(CXXFLAGS) $(INCPATH) $< -o $@ 

libdownloader.so: downloader.o confighandler.o
	$(CXX) $(SHAREDFLAGS) -o $@ $^ $(LIBS)

libunpacker.so: unpacker.o confighandler.o
	$(CXX) $(SHAREDFLAGS) -o $@ $^ $(LIBS)

libstorer.so: storer.o confighandler.o databasehandler.o
	$(CXX) $(SHAREDFLAGS) -o $@ $^ $(LIBS)

libfeatcalc.so: featurecalculator.o confighandler.o databasehandler.o
	$(CXX) $(SHAREDFLAGS) -o $@ $^ $(LIBS)

liblabelimporter.so: labelimporter.o confighandler.o databasehandler.o
	$(CXX) $(SHAREDFLAGS) -o $@ $^ $(LIBS)

libtrainer.so: trainer.o confighandler.o databasehandler.o
	$(CXX) $(SHAREDFLAGS) -o $@ $^ $(LIBS)


