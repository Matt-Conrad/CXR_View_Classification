#ifndef DATASETDOWNLOADER_H
#define DATASETDOWNLOADER_H

#include <QObject>
#include <string>
#include <unordered_map>
#include <filesystem>
#include <iostream>
#include <curl/curl.h>

const std::unordered_map<std::string, uint64_t> expected_sizes = {
        {"NLMCXR_subset_dataset.tgz", 88320855},
        {"NLMCXR_dcm.tgz", 80694582486}
    };

const std::unordered_map<std::string, uint16_t> expected_num_files_in_dataset = {
        {"NLMCXR_subset_dataset.tgz", 10},
        {"NLMCXR_dcm.tgz", 7470}
    };

class Downloader : public QObject
{
    Q_OBJECT
friend class AppController;

public:
    Downloader(std::string url, std::string filename_fullpath);
    void downloadDataset();

private:
    std::string url;
    std::string filename_fullpath;

    const uint64_t expected_size = expected_sizes.at("NLMCXR_subset_dataset.tgz");
    const uint16_t expected_num_files = expected_num_files_in_dataset.at("NLMCXR_subset_dataset.tgz");

    int download();

public slots:
    void getDataset();

signals:
    void finished();
};

#endif // DATASETDOWNLOADER_H
