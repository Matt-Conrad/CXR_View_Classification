#ifndef DATASETDOWNLOADER_H
#define DATASETDOWNLOADER_H

#include <QObject>
#include <string>
#include <filesystem>
#include <iostream>
#include <QtNetwork>

const std::unordered_map<std::string, uint64_t> expected_sizes = {
        {"NLMCXR_subset_dataset.tgz", 88320855},
        {"NLMCXR_dcm.tgz", 80694582486}
    };

class Downloader : public QObject
{
    Q_OBJECT
friend class AppController;

public:
    Downloader(std::string url, std::string filename_fullpath, std::string filename);
    void downloadDataset();

private:
    std::string url;
    std::string filename_fullpath;
    std::string dataset;
    std::string filename;

    quint64 expected_size;

    int download();

    quint64 getTgzMax();
    quint64 getTgzSize();

public slots:
    void getDataset();

signals:
    void finished();
    void attemptUpdateProBarValue(quint64);
    void attemptUpdateProBarBounds(quint64, quint64);
    void attemptUpdateText(QString);
};

#endif // DATASETDOWNLOADER_H
