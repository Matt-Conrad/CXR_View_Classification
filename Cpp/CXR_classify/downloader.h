#ifndef DATASETDOWNLOADER_H
#define DATASETDOWNLOADER_H

#include <QObject>
#include <string>
#include <filesystem>
#include <iostream>
#include <curl/curl.h>

class Downloader : public QObject
{
    Q_OBJECT
friend class AppController;

public:
    Downloader(std::string url, std::string filename_fullpath, std::string filename);
    void downloadDataset();

private:
    std::string url;
    std::string filename_fullpath;
    std::string dataset;

    int download();

public slots:
    void getDataset();

signals:
    void finished();
    void requestStartDashboard(QString, quint64, quint64);
    void sendProBarUpdate(quint64);
};

#endif // DATASETDOWNLOADER_H
