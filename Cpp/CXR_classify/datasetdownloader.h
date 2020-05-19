#ifndef DATASETDOWNLOADER_H
#define DATASETDOWNLOADER_H

#include <QObject>
#include <string>
#include <unordered_map>
#include <boost/dll/runtime_symbol_info.hpp>
#include <filesystem>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <curl/curl.h>

const std::unordered_map<std::string, uint64_t> expected_sizes = {
        {"NLMCXR_subset_dataset.tgz", 88320855},
        {"NLMCXR_dcm.tgz", 80694582486}
    };

const std::unordered_map<std::string, uint16_t> expected_num_files_in_dataset = {
        {"NLMCXR_subset_dataset.tgz", 10},
        {"NLMCXR_dcm.tgz", 7470}
    };

class DatasetDownloader : public QObject
{
    Q_OBJECT
friend class AppController;

public:
    DatasetDownloader(std::string url);
    void downloadDataset();

private:
    std::string url;
    std::string parentFolder;
    std::string filename;
    std::string filename_fullpath;
    std::string folder_name;
    std::string folder_full_path;
    std::string columns_info_name;
    std::string columns_info_full_path;

    const uint64_t expected_size = expected_sizes.at("NLMCXR_subset_dataset.tgz");
    const uint16_t expected_num_files = expected_num_files_in_dataset.at("NLMCXR_subset_dataset.tgz");

    int download();

public slots:
    void getDataset();
    void unpack();

signals:
    void finished();
};

#endif // DATASETDOWNLOADER_H
