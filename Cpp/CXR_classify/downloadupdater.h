#ifndef DOWNLOADUPDATER_H
#define DOWNLOADUPDATER_H

#include <QObject>
#include <filesystem>
#include <unordered_map>
#include <iostream>

const std::unordered_map<std::string, uint64_t> expected_sizes = {
        {"NLMCXR_subset_dataset.tgz", 88320855},
        {"NLMCXR_dcm.tgz", 80694582486}
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
    std::string filename;

    quint64 expected_size;

    quint64 getTgzMax();
    quint64 getTgzSize();

public slots:
    void updateProgressBar();

signals:
    void finished();
    void attemptUpdateProBarValue(quint64);
    void attemptUpdateProBarBounds(quint64, quint64);
    void attemptUpdateText(QString);
};

#endif // DOWNLOADUPDATER_H
