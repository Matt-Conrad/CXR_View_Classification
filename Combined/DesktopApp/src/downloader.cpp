#include "downloader.h"

Downloader::Downloader()
{
    filenameRelPath = "./" + configHandler->getTgzFilename();
    expected_size = expected_sizes.at(configHandler->getDatasetType());
}

void Downloader::run()
{
    if (std::filesystem::exists(filenameRelPath) && !std::filesystem::is_directory(filenameRelPath)) {
        if (std::filesystem::file_size(filenameRelPath) == expected_size) {
            ;
        } else {
            std::filesystem::remove(filenameRelPath);
            download();
        }
    } else {
        download();
    }
}

int Downloader::download()
{
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

Downloader * Downloader_new() {
    return new Downloader();
}

void Downloader_run(Downloader * downloader) {
    downloader->run();
}
