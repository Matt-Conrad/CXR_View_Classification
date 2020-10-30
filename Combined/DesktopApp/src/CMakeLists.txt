cmake_minimum_required(VERSION 3.10)

# set the project name
project(unpacker)

# specify the C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

include(GNUInstallDirs)

add_library(unpacker SHARED
    unpacker.cpp
    confighandler.cpp
)

target_link_libraries(unpacker -lz -lbz2 -larchive -lboost_system -lstdc++fs)

set_target_properties(unpacker PROPERTIES PUBLIC_HEADER unpacker.h)

configure_file(unpacker.pc.in unpacker.pc @ONLY)

target_include_directories(unpacker PRIVATE src)
target_include_directories(unpacker PRIVATE cmake_build)

install(TARGETS unpacker
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    PUBLIC_HEADER DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

install(FILES ${CMAKE_BINARY_DIR}/unpacker.pc DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/pkgconfig)



