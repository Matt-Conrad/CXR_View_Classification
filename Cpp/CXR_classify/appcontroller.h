#ifndef APPCONTROLLER_H
#define APPCONTROLLER_H

#include <boost/dll/runtime_symbol_info.hpp>
#include <string>
#include <filesystem>
#include <QObject>
#include <QThread>
#include <boost/property_tree/ptree.hpp>
#include "mainwindow.h"
#include "downloader.h"
#include "confighandlers.h"
#include "unpacker.h"
#include "storer.h"
#include "featurecalculator.h"
#include "labeler.h"
#include "labelimporter.h"
#include "trainer.h"
#include "basicDbOps.h"

const std::unordered_map<std::string, std::string> c_sourceUrl = {
        {"subset", "https://raw.githubusercontent.com/Matt-Conrad/CXR_View_Classification/master/datasets/NLMCXR_subset_dataset.tgz"},
        {"full_set", "https://openi.nlm.nih.gov/imgs/collections/NLMCXR_dcm.tgz"}
    };

class AppController : public QObject
{
    Q_OBJECT

    friend class MainWindow;

private:
    // String variables
    ConfigHandler * configHandler = new ConfigHandler("../CXR_classify/config.ini");
    std::string url = c_sourceUrl.at(configHandler->getSetting("dataset_info", "dataset"));

    void initGuiState();

public:
    AppController();
    ~AppController();
    Downloader * downloader = new Downloader(url, configHandler);
    Unpacker * unpacker = new Unpacker(configHandler);
    Storer * storer = new Storer(configHandler);
    FeatureCalculator * featCalc = new FeatureCalculator(configHandler);
    Labeler * labeler = new Labeler(configHandler);
    LabelImporter * labelImporter = new LabelImporter(configHandler);
    Trainer * trainer = new Trainer(configHandler);

    MainWindow mainWindow = MainWindow(this);

signals:
    void initStage1();
    void initStage2();
    void initStage3();
    void initStage4();
    void initStage5();
    void initStage6();
};

#endif // APPCONTROLLER_H
