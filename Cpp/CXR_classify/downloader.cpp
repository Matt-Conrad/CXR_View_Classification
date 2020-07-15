#include "downloader.h"

Downloader::Downloader(std::string url, std::string filename_fullpath, ConfigHandler * configHandler) : QObject()
{
    Downloader::url = url;
    Downloader::filename_fullpath = filename_fullpath;
    Downloader::filename = filename_fullpath.substr(filename_fullpath.find_last_of("/") + 1);
    Downloader::configHandler = configHandler;

    Downloader::expected_size = expected_sizes.at(filename);
}

void Downloader::getDataset()
{
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
    emit attemptUpdateText("Downloading images");
    emit attemptUpdateProBarBounds(0, getTgzMax());

    QNetworkAccessManager nam;
    QFile file(filename_fullpath.c_str());
    if(!file.open(QIODevice::ReadWrite)) {
        std::cout << "Can't open write file" << std::endl;
    }
    QNetworkRequest request(QUrl(url.c_str()));
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
    std::string dataset = configHandler->getSetting("dataset_info", "dataset");
    if (dataset == "full_set") {
        return quint64(std::filesystem::file_size(filename_fullpath) / 100);
//        return std::filesystem::file_size(filename_fullpath);
    } else if (dataset == "subset") {
        return std::filesystem::file_size(filename_fullpath);
    } else {
        return 0;
    }
}

quint64 Downloader::getTgzMax()
{
    std::string dataset = configHandler->getSetting("dataset_info", "dataset");
    if (dataset == "full_set") {
        return quint64(expected_size / 100);
//        return expected_size;
    } else if (dataset == "subset") {
        return expected_size;
    } else {
        return 0;
    }
}
