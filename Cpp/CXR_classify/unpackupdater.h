#ifndef UNPACKUPDATER_H
#define UNPACKUPDATER_H

#include <QObject>
#include <filesystem>
#include <unordered_map>

const std::unordered_map<std::string, uint16_t> expected_num_files_in_dataset = {
        {"NLMCXR_subset_dataset.tgz", 10},
        {"NLMCXR_dcm.tgz", 7470}
    };

class UnpackUpdater : public QObject
{
    Q_OBJECT

friend class AppController;

public:
    UnpackUpdater(std::string folder_full_path, std::string dataset);

private:
    std::string folder_full_path;
    std::string dataset;

    const quint64 expected_num_files = expected_num_files_in_dataset.at("NLMCXR_subset_dataset.tgz");

    quint64 countDcms();

public slots:
    void updateProgressBar();

signals:
    void finished();
    void attemptUpdateProBarValue(quint64);
    void attemptUpdateProBarBounds(quint64, quint64);
    void attemptUpdateText(QString);
};





#endif // UNPACKUPDATER_H
