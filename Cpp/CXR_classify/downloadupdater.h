#ifndef DOWNLOADUPDATER_H
#define DOWNLOADUPDATER_H

#include <QObject>
#include <filesystem>
#include <unordered_map>
#include <thread>
#include <chrono>

const std::unordered_map<std::string, uint64_t> expected_sizes = {
        {"NLMCXR_subset_dataset.tgz", 88320855},
        {"NLMCXR_dcm.tgz", 80694582486}
    };

const std::unordered_map<std::string, uint16_t> expected_num_files_in_dataset = {
        {"NLMCXR_subset_dataset.tgz", 10},
        {"NLMCXR_dcm.tgz", 7470}
    };

class DownloadUpdater : public QObject
{
    Q_OBJECT

friend class AppController;

public:
    DownloadUpdater(std::string filename_fullpath, std::string dataset);

private:
    std::string filename_fullpath;
    std::string dataset;

    const uint64_t expected_size = expected_sizes.at("NLMCXR_subset_dataset.tgz");
    const uint16_t expected_num_files = expected_num_files_in_dataset.at("NLMCXR_subset_dataset.tgz");

    quint64 getTgzMax();
    quint64 getTgzSize();

public slots:
    void updateProgressBar();

signals:
    void finished();
    void attemptUpdateProBar(quint64);
};

#endif // DOWNLOADUPDATER_H
