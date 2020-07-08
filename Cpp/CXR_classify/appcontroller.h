#ifndef APPCONTROLLER_H
#define APPCONTROLLER_H

#include <boost/dll/runtime_symbol_info.hpp>
#include <string>
#include <filesystem>
#include <QThreadPool>
#include <QObject>
#include <QThread>
#include <boost/property_tree/ptree.hpp>
#include "mainwindow.h"
#include "downloader.h"
#include "confighandlers.h"
#include "unpacker.h"
#include "downloadupdater.h"
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
    std::string configFilename = "../CXR_classify/config.ini";
    std::string dataset = config::getSection(configFilename, "dataset_info").get<std::string>("dataset");
    std::string url = c_sourceUrl.at(dataset);
    std::string parentFolder = boost::dll::program_location().parent_path().string();
    std::string filename = url.substr(url.find_last_of("/") + 1);
    std::string filename_fullpath = parentFolder + "/" + filename;
    std::string folder_name = filename.substr(0, filename.find_last_of("."));
    std::string folder_full_path = parentFolder + "/" + folder_name;
    std::string columns_info_name = "../CXR_classify/columns_info.json";
    std::string columns_info_full_path = parentFolder + "/" + columns_info_name;

    boost::property_tree::ptree dbInfo = config::getSection(configFilename, "postgresql");
    std::string host = config::getSection(configFilename, "postgresql").get<std::string>("host");
    std::string port = config::getSection(configFilename, "postgresql").get<std::string>("port");
    std::string database = config::getSection(configFilename, "postgresql").get<std::string>("database");
    std::string user = config::getSection(configFilename, "postgresql").get<std::string>("user");
    std::string password = config::getSection(configFilename, "postgresql").get<std::string>("password");

    // From config file
    std::string dbName = config::getSection(configFilename, "postgresql").get<std::string>("database");
    std::string metaTableName = config::getSection(configFilename, "table_info").get<std::string>("metadata_table_name");
    std::string featTableName = config::getSection(configFilename, "table_info").get<std::string>("features_table_name");
    std::string labelTableName = config::getSection(configFilename, "table_info").get<std::string>("label_table_name");

    void initGuiState();
    QThreadPool threadpool = QThreadPool();

public:
    AppController();
    Downloader * downloader = new Downloader(url, filename_fullpath, dataset);
    DownloadUpdater * downloadUpdater = new DownloadUpdater(filename_fullpath, dataset);
    Unpacker * unpacker = new Unpacker(filename_fullpath, folder_full_path, parentFolder, dataset, filename);
    Storer * storer = new Storer(columns_info_name, configFilename, "elements", folder_full_path, filename);
    FeatureCalculator * featCalc = new FeatureCalculator(columns_info_name, configFilename, "elements", folder_full_path, filename);
    Labeler * labeler = new Labeler(configFilename, columns_info_name);
    LabelImporter * labelImporter = new LabelImporter(labelTableName, (parentFolder + "/../CXR_classify/image_labels.csv"), columns_info_full_path, configFilename, "labels");
    Trainer * trainer = new Trainer(configFilename, featTableName, labelTableName, filename);

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
