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
    std::string parentFolder = boost::dll::program_location().parent_path().string();
    std::string filename = url.substr(url.find_last_of("/") + 1);
    std::string filename_fullpath = parentFolder + "/" + filename;
    std::string folder_name = filename.substr(0, filename.find_last_of("."));
    std::string folder_full_path = parentFolder + "/" + folder_name;
    std::string columns_info_name = "../CXR_classify/columns_info.json";
    std::string columns_info_full_path = parentFolder + "/" + columns_info_name;
    std::string csvFullPath = parentFolder + "/../CXR_classify/image_labels.csv";

    void initGuiState();

public:
    AppController();
    Downloader * downloader = new Downloader(url, filename_fullpath, configHandler);
    Unpacker * unpacker = new Unpacker(filename_fullpath, folder_full_path, parentFolder, filename, configHandler);
    Storer * storer = new Storer(columns_info_name, folder_full_path, filename, configHandler);
    FeatureCalculator * featCalc = new FeatureCalculator(columns_info_name, folder_full_path, filename, configHandler);
    Labeler * labeler = new Labeler(columns_info_name, configHandler);
    LabelImporter * labelImporter = new LabelImporter(csvFullPath, columns_info_full_path, configHandler);
    Trainer * trainer = new Trainer(filename, configHandler);

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
