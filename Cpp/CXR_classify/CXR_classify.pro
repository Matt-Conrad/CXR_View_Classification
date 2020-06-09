QT += widgets

QMAKE_CXXFLAGS += -std=c++17

CONFIG += console
CONFIG -= app_bundle

# The following define makes your compiler emit warnings if you use
# any Qt feature that has been marked deprecated (the exact warnings
# depend on your compiler). Please consult the documentation of the
# deprecated API in order to know how to port your code away from it.
DEFINES += QT_DEPRECATED_WARNINGS

INCLUDEPATH += /usr/local/include/opencv4

# You can also make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
# You can also select to disable deprecated APIs only up to a certain version of Qt.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

SOURCES += \
        appcontroller.cpp \
        confighandlers.cpp \
        downloader.cpp \
        downloadupdater.cpp \
        featcalcupdater.cpp \
        featurecalculator.cpp \
        main.cpp \
        mainwindow.cpp \
        storer.cpp \
        storeupdater.cpp \
        unpacker.cpp \
        unpackupdater.cpp

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target

HEADERS += \
    appcontroller.h \
    confighandlers.h \
    downloader.h \
    downloadupdater.h \
    featcalcupdater.h \
    featurecalculator.h \
    mainwindow.h \
    storer.h \
    storeupdater.h \
    unpacker.h \
    unpackupdater.h

LIBS += -ldl -lboost_system -lboost_filesystem -lstdc++fs  -lcurl -lz -lbz2  -larchive -lpqxx -lpq -pthread -ldcmimgle -ldcmdata -loflog -lofstd -lz -liconv -lcharset -lopencv_core -lopencv_imgproc -lopencv_highgui

DISTFILES += \
    columns_info.json \
    config.ini
