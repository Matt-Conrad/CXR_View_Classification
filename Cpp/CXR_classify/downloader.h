#ifndef DATASETDOWNLOADER_H
#define DATASETDOWNLOADER_H

#include <QObject>
#include <string>
#include <filesystem>
#include <QtNetwork>
#include "expectedsizes.h"
#include "confighandlers.h"

class Downloader : public QObject
{
    Q_OBJECT
friend class AppController;

public:
    Downloader(ConfigHandler *);

private:
    quint64 expected_size;

    ConfigHandler * configHandler;

    std::string filenameRelPath;
    std::string datasetType;

    int download();

    quint64 getTgzMax();
    quint64 getTgzSize();

public slots:
    void getDataset();

signals:
    void finished();
    void attemptUpdateProBarValue(quint64);
    void attemptUpdateProBarBounds(quint64, quint64);
    void attemptUpdateText(QString);
};

#endif // DATASETDOWNLOADER_H
