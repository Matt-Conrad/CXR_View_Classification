#include "downloadupdater.h"

DownloadUpdater::DownloadUpdater(std::string filename_fullpath, std::string dataset)
{
    DownloadUpdater::filename_fullpath = filename_fullpath;
    DownloadUpdater::dataset = dataset;
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
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }
    emit attemptUpdateProBarValue(getTgzSize());
    emit attemptUpdateText("Image download complete");

    emit finished();
}


quint64 DownloadUpdater::getTgzSize()
{
    if (dataset == "full_set") {
        return int(std::filesystem::file_size(filename_fullpath) / 100);
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
    } else if (dataset == "subset") {
        return expected_size;
    } else {
        return 0;
    }
}
