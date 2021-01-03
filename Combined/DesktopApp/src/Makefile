# Manually created 
CXX := g++
CXXFLAGS := -std=c++17 -fPIC -fopenmp -c 
SHAREDFLAGS = -shared -Wl,-soname,$@ -Wl,-rpath=/opt/qt515/lib -L/opt/qt515/lib

SOURCES := confighandler.cpp \
    databasehandler.cpp \
	downloader.cpp \
	unpacker.cpp \
	storer.cpp \
	featurecalculator.cpp \
	labelimporter.cpp \
	trainer.cpp

SOURCE_DIR := ../src

SHARED_OBJS_WITHOUT_DBHANDLER := libdownloader.so \
	libunpacker.so

SHARED_OBJS_WITH_DBHANDLER := libstorer.so \
	libfeaturecalculator.so \
	liblabelimporter.so \
	libtrainer.so

SHARED_OBJS := $(SHARED_OBJS_WITHOUT_DBHANDLER) $(SHARED_OBJS_WITH_DBHANDLER)

OBJS := ${SOURCES:cpp=o} 

LIBS:= -lQt5Network -lQt5Core -lopencv_core -lopencv_imgproc -lz -lbz2 -larchive -ldcmimgle -ldcmdata -lpqxx -lpq -larmadillo -lmlpack -lboost_system -lstdc++fs 

INCPATH := -I/opt/qt515/include -I/opt/qt515/include/QtNetwork -I/opt/qt515/include/QtCore 
INCPATH += -I/usr/include/opencv4

.PHONY: all clean clean_objects

all: ${OBJS} ${SHARED_OBJS}

clean :
	rm -f *.o *.so

clean_objects :
	rm -f *.o

$(OBJS): %.o : $(SOURCE_DIR)/%.cpp $(SOURCE_DIR)/%.h $(SOURCE_DIR)/expectedsizes.h
	$(CXX) $(CXXFLAGS) $(INCPATH) $< -o $@ 

$(SHARED_OBJS): lib%.so : %.o confighandler.o
	$(CXX) $(SHAREDFLAGS) -o $@ $^ $(LIBS)

$(SHARED_OBJS_WITH_DBHANDLER): lib%.so : databasehandler.o