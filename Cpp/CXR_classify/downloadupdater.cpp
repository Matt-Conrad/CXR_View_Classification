#include "downloadupdater.h"

DownloadUpdater::DownloadUpdater(std::string filename_fullpath, std::string dataset)
{
    DownloadUpdater::filename_fullpath = filename_fullpath;
    DownloadUpdater::dataset = dataset;
    DownloadUpdater::filename = filename_fullpath.substr(filename_fullpath.find_last_of("/") + 1);
    DownloadUpdater::expected_size = expected_sizes.at(filename);
}

void DownloadUpdater::updateProgressBar()
{
    emit attemptUpdateText("Downloading images");
    emit attemptUpdateProBarBounds(0, getTgzMax());

    while (!std::filesystem::exists(filename_fullpath)) {
        ;
    }

    emit attemptUpdateProBarValue(0);
    while (getTgzSize() < getTgzMax()) {
        emit attemptUpdateProBarValue(getTgzSize());
    }
    emit attemptUpdateProBarValue(getTgzSize());
    emit attemptUpdateText("Image download complete");

    emit finished();
}


quint64 DownloadUpdater::getTgzSize()
{
    if (dataset == "full_set") {
        return quint64(std::filesystem::file_size(filename_fullpath) / 100);
//        return std::filesystem::file_size(filename_fullpath);
    } else if (dataset == "subset") {
        return std::filesystem::file_size(filename_fullpath);
    } else {
        return 0;
    }
}

quint64 DownloadUpdater::getTgzMax()
{
    if (dataset == "full_set") {
        return quint64(expected_size / 100);
//        return expected_size;
    } else if (dataset == "subset") {
        return expected_size;
    } else {
        return 0;
    }
}
