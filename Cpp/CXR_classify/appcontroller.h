#ifndef APPCONTROLLER_H
#define APPCONTROLLER_H

#include <string>
#include <filesystem>
#include <QObject>
#include "mainwindow.h"
#include "downloader.h"
#include "confighandler.h"
#include "unpacker.h"
#include "storer.h"
#include "featurecalculator.h"
#include "labeler.h"
#include "labelimporter.h"
#include "trainer.h"
#include "databasehandler.h"
#include "expectedsizes.h"

class AppController : public QObject
{
    Q_OBJECT

    friend class MainWindow;

private:
    // String variables
    ConfigHandler * configHandler = new ConfigHandler("../CXR_classify/config.ini");
    DatabaseHandler * dbHandler = new DatabaseHandler(configHandler);

public:
    AppController();
    ~AppController();
    Downloader * downloader = new Downloader(configHandler);
    Unpacker * unpacker = new Unpacker(configHandler);
    Storer * storer = new Storer(configHandler, dbHandler);
    FeatureCalculator * featCalc = new FeatureCalculator(configHandler, dbHandler);
    Labeler * labeler = new Labeler(configHandler, dbHandler);
    LabelImporter * labelImporter = new LabelImporter(configHandler, dbHandler);
    Trainer * trainer = new Trainer(configHandler, dbHandler);

    MainWindow mainWindow = MainWindow(this);
};

#endif // APPCONTROLLER_H
