QT += widgets
QT += network

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
        confighandler.cpp \
        databasehandler.cpp \
        downloader.cpp \
        downloadstage.cpp \
        featurecalculator.cpp \
        featurecalculatorstage.cpp \
        labelimporter.cpp \
        labelstage.cpp \
        main.cpp \
        mainwindow.cpp \
        manuallabeler.cpp \
        runnable.cpp \
        stage.cpp \
        storer.cpp \
        storestage.cpp \
        trainer.cpp \
        trainstage.cpp \
        unpacker.cpp \
        unpackstage.cpp

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target

HEADERS += \
    confighandler.h \
    databasehandler.h \
    downloader.h \
    downloadstage.h \
    expectedsizes.h \
    featurecalculator.h \
    featurecalculatorstage.h \
    labelimporter.h \
    labelstage.h \
    mainwindow.h \
    manuallabeler.h \
    runnable.h \
    stage.h \
    storer.h \
    storestage.h \
    trainer.h \
    trainstage.h \
    unpacker.h \ \
    unpackstage.h

LIBS += -ldl -lboost_system -lstdc++fs -lz -lbz2 -larchive -lpqxx -lpq -pthread -ldcmimgle -ldcmdata -loflog -lofstd -lopencv_cudaarithm -lopencv_core -lopencv_imgproc -fopenmp -larmadillo -lmlpack

DISTFILES += \
    ../../miscellaneous/columns_info.json \
    ../../miscellaneous/config.ini \
    ../../miscellaneous/image_labels.csv

