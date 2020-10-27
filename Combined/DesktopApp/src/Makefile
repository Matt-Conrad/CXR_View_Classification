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

SHARED_OBJS_WITHOUT_DBHANDLER = libdownloader.so \
	libunpacker.so

SHARED_OBJS_WITH_DBHANDLER = libstorer.so \
	libfeaturecalculator.so \
	liblabelimporter.so \
	libtrainer.so

SHARED_OBJS = $(SHARED_OBJS_WITHOUT_DBHANDLER) $(SHARED_OBJS_WITH_DBHANDLER)

OBJS := ${SRCS:cpp=o} 

LIBS = -lQt5Network -lQt5Core -lopencv_core -lopencv_imgproc -lz -lbz2 -larchive -ldcmimgle -ldcmdata -lpqxx -lpq -fopenmp -larmadillo -lmlpack -lboost_system -lstdc++fs 

INCPATH = -I/home/matthew/Qt5/5.15.1/gcc_64/include -I/home/matthew/Qt5/5.15.1/gcc_64/include/QtNetwork -I/home/matthew/Qt5/5.15.1/gcc_64/include/QtCore 
INCPATH += -I/usr/local/include/opencv4

.PHONY: all clean

all: ${OBJS} ${SHARED_OBJS}

clean :
	rm -f *.o *.so

$(OBJS): %.o : %.cpp %.h expectedsizes.h
	$(CXX) $(CXXFLAGS) $(INCPATH) $< -o $@ 

$(SHARED_OBJS): lib%.so : %.o confighandler.o
	$(CXX) $(SHAREDFLAGS) -o $@ $^ $(LIBS)

$(SHARED_OBJS_WITH_DBHANDLER): lib%.so : databasehandler.o