#include "downloadupdater.h"

DownloadUpdater::DownloadUpdater(std::string filename_fullpath, std::string dataset)
{
    DownloadUpdater::filename_fullpath = filename_fullpath;
    DownloadUpdater::dataset = dataset;
}

void DownloadUpdater::updateProgressBar()
{
    while (!std::filesystem::exists(filename_fullpath)) {
        ;
    }

    emit attemptUpdateProBar(0);
    while (getTgzSize() < getTgzMax()) {
        emit attemptUpdateProBar(getTgzSize());
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }
    emit attemptUpdateProBar(getTgzSize());

    emit finished();

//    centralWidget->findChild<QLabel *>("msgBox")->setText("Image download complete");

//    centralWidget->findChild<QPushButton *>("downloadBtn")->setDisabled(true);
//    centralWidget->findChild<QPushButton *>("unpackBtn")->setDisabled(false);
//    centralWidget->findChild<QPushButton *>("storeBtn")->setDisabled(true);
//    centralWidget->findChild<QPushButton *>("featuresBtn")->setDisabled(true);
//    centralWidget->findChild<QPushButton *>("labelBtn")->setDisabled(true);
//    centralWidget->findChild<QPushButton *>("classifyBtn")->setDisabled(true);
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
        return int(expected_size / 100);
    } else if (dataset == "subset") {
        return expected_size;
    } else {
        return 0;
    }
}
