#include "downloader.h"

Downloader::Downloader(ConfigHandler * configHandler) : Runnable(configHandler)
{
    filenameRelPath = "./" + configHandler->getTgzFilename();
    datasetType = configHandler->getDatasetType();
}

void Downloader::run()
{
    if (std::filesystem::exists(filenameRelPath) && !std::filesystem::is_directory(filenameRelPath)) {
        if (std::filesystem::file_size(filenameRelPath) == expected_size) { // replace hard code with expected size
            // log "File  was downloaded properly"
        } else {
            std::filesystem::remove(filenameRelPath);
            download();
        }
    } else {
        download();
    }
    emit signalOptions->attemptUpdateProBarValue(getTgzSize());
    emit signalOptions->attemptUpdateText("Image download complete");
    emit signalOptions->finished();
}

int Downloader::download()
{
    emit signalOptions->attemptUpdateText("Downloading images");
    emit signalOptions->attemptUpdateProBarBounds(0, getTgzMax());

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
        emit signalOptions->attemptUpdateProBarValue(getTgzSize());
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
