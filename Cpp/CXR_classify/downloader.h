#ifndef DOWNLOADER_H
#define DOWNLOADER_H

#include <QObject>
#include <string>
#include <filesystem>
#include <QtNetwork>
#include "confighandler.h"
#include "runnable.h"

class Downloader : public Runnable
{
public:
    Downloader(ConfigHandler *);

private:
    std::string filenameRelPath;
    std::string datasetType;

    int download();

    quint64 getTgzMax();
    quint64 getTgzSize();

public slots:
    void run();
};

#endif // DOWNLOADER_H
