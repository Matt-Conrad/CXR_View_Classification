#ifndef DATASETDOWNLOADER_H
#define DATASETDOWNLOADER_H

#include <QObject>
#include <string>
#include <filesystem>
#include <QtNetwork>
#include "confighandler.h"
#include "stage.h"

class Downloader : public Stage
{
    Q_OBJECT

friend class AppController;

public:
    Downloader(ConfigHandler *);

private:
    std::string filenameRelPath;
    std::string datasetType;

    int download();

    quint64 getTgzMax();
    quint64 getTgzSize();

public slots:
    void getDataset();
};

#endif // DATASETDOWNLOADER_H
