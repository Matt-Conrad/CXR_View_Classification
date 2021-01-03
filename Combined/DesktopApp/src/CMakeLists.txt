cmake_minimum_required(VERSION 3.10)

# set the project name
project(CXR_classify)

# specify the C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fopenmp")

# FIND OPENCV AND QT SO DON'T HAVE TO HARDCODE THEM

add_library(downloader SHARED
    downloader.cpp
    confighandler.cpp
)

add_library(unpacker SHARED
    unpacker.cpp
    confighandler.cpp
)

add_library(storer SHARED
    storer.cpp
    confighandler.cpp
    databasehandler.cpp
)

add_library(featurecalculator SHARED
    featurecalculator.cpp
    confighandler.cpp
    databasehandler.cpp
)

add_library(labelimporter SHARED
    labelimporter.cpp
    confighandler.cpp
    databasehandler.cpp
)

add_library(trainer SHARED
    trainer.cpp
    confighandler.cpp
    databasehandler.cpp
)

target_include_directories(downloader PRIVATE src)
target_include_directories(downloader PRIVATE /opt/qt515/include)
target_include_directories(downloader PRIVATE /opt/qt515/include/QtNetwork)
target_include_directories(unpacker PRIVATE src)
target_include_directories(storer PRIVATE src)
target_include_directories(featurecalculator PRIVATE src)
target_include_directories(featurecalculator PRIVATE /usr/include/opencv4)
target_include_directories(featurecalculator PRIVATE /opt/qt515/include)
target_include_directories(featurecalculator PRIVATE /opt/qt515/include/QtCore)
target_include_directories(labelimporter PRIVATE src)
target_include_directories(trainer PRIVATE src)
target_include_directories(trainer PRIVATE /opt/qt515/include)
target_include_directories(trainer PRIVATE /opt/qt515/include/QtCore)

target_link_libraries(downloader -lQt5Network -lQt5Core -lboost_system -lstdc++fs)
target_link_libraries(unpacker -lz -lbz2 -larchive -lboost_system -lstdc++fs)
target_link_libraries(storer -ldcmimgle -ldcmdata -lpqxx -lpq -lboost_system -lstdc++fs)
target_link_libraries(featurecalculator -lQt5Core -ldcmimgle -ldcmdata -lopencv_core -lopencv_imgproc -lpqxx -lpq -lboost_system -lstdc++fs)
target_link_libraries(labelimporter -lpqxx -lpq -lboost_system -lstdc++fs)
target_link_libraries(trainer -lQt5Core -lpqxx -lpq -larmadillo -lmlpack -lboost_system -lstdc++fs)

set_target_properties(downloader PROPERTIES LINK_FLAGS "-Wl,-rpath=/opt/qt515/lib -L/opt/qt515/lib")
set_target_properties(featurecalculator PROPERTIES LINK_FLAGS "-Wl,-rpath=/opt/qt515/lib -L/opt/qt515/lib")
set_target_properties(trainer PROPERTIES LINK_FLAGS "-Wl,-rpath=/opt/qt515/lib -L/opt/qt515/lib")




