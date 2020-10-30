cmake_minimum_required(VERSION 3.10)

# set the project name
project(CXR_classify)

# specify the C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

include(GNUInstallDirs)

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

target_link_libraries(downloader -lQt5Network -lQt5Core -lboost_system -lstdc++fs)
target_link_libraries(unpacker -lz -lbz2 -larchive -lboost_system -lstdc++fs)
target_link_libraries(storer -ldcmimgle -ldcmdata -lpqxx -lpq -lboost_system -lstdc++fs)
target_link_libraries(featurecalculator -ldcmimgle -ldcmdata -lopencv_core -lopencv_imgproc -lpqxx -lpq -lboost_system -lstdc++fs)
target_link_libraries(labelimporter -lpqxx -lpq -lboost_system -lstdc++fs)
target_link_libraries(trainer -lpqxx -lpq -fopenmp -larmadillo -lmlpack -lboost_system -lstdc++fs)

set_target_properties(downloader PROPERTIES PUBLIC_HEADER downloader.h)
set_target_properties(unpacker PROPERTIES PUBLIC_HEADER unpacker.h)
set_target_properties(storer PROPERTIES PUBLIC_HEADER storer.h)
set_target_properties(featurecalculator PROPERTIES PUBLIC_HEADER featurecalculator.h)
set_target_properties(labelimporter PROPERTIES PUBLIC_HEADER labelimporter.h)
set_target_properties(trainer PROPERTIES PUBLIC_HEADER trainer.h)

configure_file(downloader.pc.in downloader.pc @ONLY)
configure_file(unpacker.pc.in unpacker.pc @ONLY)
configure_file(storer.pc.in storer.pc @ONLY)
configure_file(featurecalculator.pc.in featurecalculator.pc @ONLY)
configure_file(labelimporter.pc.in labelimporter.pc @ONLY)
configure_file(trainer.pc.in trainer.pc @ONLY)

# set(CMAKE_BUILD_RPATH "/home/matthew/Qt5/5.15.1/gcc_64/lib")
set_target_properties(downloader PROPERTIES LINK_FLAGS "-Wl,-rpath,/home/matthew/Qt5/5.15.1/gcc_64/lib")

target_include_directories(downloader PRIVATE src)
target_include_directories(downloader PRIVATE cmake_build)
target_include_directories(downloader PRIVATE /home/matthew/Qt5/5.15.1/gcc_64/include)
target_include_directories(downloader PRIVATE /home/matthew/Qt5/5.15.1/gcc_64/include/QtNetwork)
target_include_directories(downloader PRIVATE /home/matthew/Qt5/5.15.1/gcc_64/include/QtCore)
target_include_directories(unpacker PRIVATE src)
target_include_directories(unpacker PRIVATE cmake_build)
target_include_directories(storer PRIVATE src)
target_include_directories(storer PRIVATE cmake_build)
target_include_directories(featurecalculator PRIVATE src)
target_include_directories(featurecalculator PRIVATE cmake_build)
target_include_directories(featurecalculator PRIVATE /usr/local/include/opencv4)
target_include_directories(labelimporter PRIVATE src)
target_include_directories(labelimporter PRIVATE cmake_build)
target_include_directories(trainer PRIVATE src)
target_include_directories(trainer PRIVATE cmake_build)

install(TARGETS downloader
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

install(TARGETS unpacker
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

install(TARGETS storer
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

install(TARGETS featurecalculator
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

install(TARGETS labelimporter
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

install(TARGETS trainer
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

install(FILES ${CMAKE_BINARY_DIR}/downloader.pc DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/pkgconfig)
install(FILES ${CMAKE_BINARY_DIR}/unpacker.pc DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/pkgconfig)
install(FILES ${CMAKE_BINARY_DIR}/storer.pc DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/pkgconfig)
install(FILES ${CMAKE_BINARY_DIR}/featurecalculator.pc DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/pkgconfig)
install(FILES ${CMAKE_BINARY_DIR}/labelimporter.pc DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/pkgconfig)
install(FILES ${CMAKE_BINARY_DIR}/trainer.pc DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/pkgconfig)



