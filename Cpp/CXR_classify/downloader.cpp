#include "downloader.h"

#include <chrono>
#include <iostream>

namespace fs = std::filesystem;

Downloader::Downloader(ConfigHandler * configHandler) : Runnable(configHandler)
{
    filenameAbsPath = configHandler->getTgzFilePath();
    datasetType = configHandler->getDatasetType();
}

void Downloader::run()
{
    // std::chrono::steady_clock::time_point begin = std::chrono::steady_clock::now();
    logger->info("Checking if {} already exists", filenameAbsPath);
    if (fs::exists(filenameAbsPath) && !fs::is_directory(filenameAbsPath)) {
        logger->info("{} already exists", filenameAbsPath);
        logger->info("Checking if {} was downloaded properly", filenameAbsPath);
        if (fs::file_size(filenameAbsPath) == expected_size) {
            logger->info("{} was downloaded properly", filenameAbsPath);
        } else {
            logger->warn("{} was not downloaded properly", filenameAbsPath);
            logger->info("Removing {}", filenameAbsPath);
            fs::remove(filenameAbsPath);
            logger->info("Successfully removed {}", filenameAbsPath);
            download();
        }
    } else {
        logger->info("{} does not exist", filenameAbsPath);
        download();
    }
    // std::chrono::steady_clock::time_point end = std::chrono::steady_clock::now();
    // std::cout << "Time difference = " << (std::chrono::duration_cast<std::chrono::nanoseconds> (end - begin).count())/1000000000.0 << "[s]" << std::endl;
    emit attemptUpdateProBarValue(getTgzSize());
    emit attemptUpdateText("Image download complete");
    emit finished();
}

int Downloader::download()
{
    logger->info("Downloading dataset from {}", configHandler->getUrl());

    emit attemptUpdateText("Downloading images");
    emit attemptUpdateProBarBounds(0, getTgzMax());

    QNetworkAccessManager nam;
    QFile file(filenameAbsPath.c_str());
    if(!file.open(QIODevice::ReadWrite)) {
        // log "Can't open write file"
    }
    QNetworkRequest request(QUrl(configHandler->getUrl().c_str()));
    QNetworkReply* reply = nam.get(request);
    QEventLoop event;

    QObject::connect(reply, &QNetworkReply::readyRead, [&]{
        //this will be called every time a chunk of data is received
        QByteArray data= reply->readAll();
        emit attemptUpdateProBarValue(getTgzSize());
        file.write(data);
    });

    //use the finished signal from the reply object to close the file
    //and delete the reply object
    QObject::connect(reply, &QNetworkReply::finished, [&]{
        QByteArray data= reply->readAll();
        file.write(data);
        file.close();
        reply->deleteLater();
        event.quit();
    });

    event.exec();

    // At some point should call run again, similar to python implementation

    return 0;
}

quint64 Downloader::getTgzSize()
{
    if (datasetType == "full_set") {
        return quint64(fs::file_size(filenameAbsPath) / 100);
    } else if (datasetType == "subset") {
        return fs::file_size(filenameAbsPath);
    } else {
        return 0;
    }
}

quint64 Downloader::getTgzMax()
{
    if (datasetType == "full_set") {
        return quint64(expected_size / 100);
    } else if (datasetType == "subset") {
        return expected_size;
    } else {
        return 0;
    }
}
