#include "downloader.h"

Downloader::Downloader(ConfigHandler * configHandler) : QObject()
{
    Downloader::configHandler = configHandler;

    Downloader::expected_size = expected_sizes.at(configHandler->getTgzFilename());
}

void Downloader::getDataset()
{
    std::string filename_fullpath = configHandler->getParentFolder() + "/" + configHandler->getTgzFilename();
    if (std::filesystem::exists(filename_fullpath) && !std::filesystem::is_directory(filename_fullpath)) {
        if (std::filesystem::file_size(filename_fullpath) == 88320855) { // replace hard code with expected size
            std::cout << "File  was downloaded properly" << std::endl;
        } else {
            std::filesystem::remove(filename_fullpath);
            Downloader::downloadDataset();
        }
    } else {
        Downloader::downloadDataset();
    }
    emit attemptUpdateProBarValue(getTgzSize());
    emit attemptUpdateText("Image download complete");
    emit finished();
}

void Downloader::downloadDataset()
{
    download();
}

int Downloader::download()
{
    std::string filename_fullpath = configHandler->getParentFolder() + "/" + configHandler->getTgzFilename();

    emit attemptUpdateText("Downloading images");
    emit attemptUpdateProBarBounds(0, getTgzMax());

    QNetworkAccessManager nam;
    QFile file(filename_fullpath.c_str());
    if(!file.open(QIODevice::ReadWrite)) {
        std::cout << "Can't open write file" << std::endl;
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
    return 0;
}

quint64 Downloader::getTgzSize()
{
    std::string filename_fullpath = configHandler->getParentFolder() + "/" + configHandler->getTgzFilename();

    if (configHandler->getDatasetType() == "full_set") {
        return quint64(std::filesystem::file_size(filename_fullpath) / 100);
    } else if (configHandler->getDatasetType() == "subset") {
        return std::filesystem::file_size(filename_fullpath);
    } else {
        return 0;
    }
}

quint64 Downloader::getTgzMax()
{
    if (configHandler->getDatasetType() == "full_set") {
        return quint64(expected_size / 100);
//        return expected_size;
    } else if (configHandler->getDatasetType() == "subset") {
        return expected_size;
    } else {
        return 0;
    }
}
