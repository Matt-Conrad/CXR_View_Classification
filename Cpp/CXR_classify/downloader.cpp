#include "downloader.h"

Downloader::Downloader(ConfigHandler * configHandler) : Runnable(configHandler)
{
    filenameRelPath = "./" + configHandler->getTgzFilename();
    datasetType = configHandler->getDatasetType();
}

void Downloader::run()
{
    logger->info("Checking if {} already exists", filenameRelPath);
    if (std::filesystem::exists(filenameRelPath) && !std::filesystem::is_directory(filenameRelPath)) {
        logger->info("{} already exists", filenameRelPath);
        logger->info("Checking if {} was downloaded properly", filenameRelPath);
        if (std::filesystem::file_size(filenameRelPath) == expected_size) {
            logger->info("{} was downloaded properly", filenameRelPath);
        } else {
            logger->warn("{} was not downloaded properly", filenameRelPath);
            logger->info("Removing {}", filenameRelPath);
            std::filesystem::remove(filenameRelPath);
            logger->info("Successfully removed {}", filenameRelPath);
            download();
        }
    } else {
        logger->info("{} does not exist", filenameRelPath);
        download();
    }
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
    QFile file(filenameRelPath.c_str());
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
        return quint64(std::filesystem::file_size(filenameRelPath) / 100);
    } else if (datasetType == "subset") {
        return std::filesystem::file_size(filenameRelPath);
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
