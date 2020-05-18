#ifndef APPCONTROLLER_H
#define APPCONTROLLER_H

#include <boost/dll/runtime_symbol_info.hpp>
#include <string>
#include <filesystem>
#include <QThreadPool>
#include "mainwindow.h"
#include "datasetdownloader.h"
#include "confighandlers.h"

const std::unordered_map<std::string, std::string> c_sourceUrl = {
        {"subset", "https://raw.githubusercontent.com/Matt-Conrad/CXR_View_Classification/master/datasets/NLMCXR_subset_dataset.tgz"},
        {"full_set", "https://openi.nlm.nih.gov/imgs/collections/NLMCXR_dcm.tgz"}
    };

class AppController
{
public:
    AppController();

private:
    // String variables
    std::string configFilename = "../CXR_classify/config.ini";
    std::string dataset = configParser(configFilename, "dataset_info").get<std::string>("dataset");
    std::string url = c_sourceUrl.at(dataset);

    // Object variables
    MainWindow mainWindow = MainWindow();
    // label_app
    // classifier
    DatasetDownloader downloader = DatasetDownloader(url);

    // From config file
    std::string dbName = configParser(configFilename, "postgresql").get<std::string>("database");
    std::string metaTableName = configParser(configFilename, "table_info").get<std::string>("metadata_table_name");
    std::string featTableName = configParser(configFilename, "table_info").get<std::string>("features_table_name");
    std::string labelTableName = configParser(configFilename, "table_info").get<std::string>("label_table_name");

    void initGuiState();
    QThreadPool threadpool = QThreadPool();
};

#endif // APPCONTROLLER_H