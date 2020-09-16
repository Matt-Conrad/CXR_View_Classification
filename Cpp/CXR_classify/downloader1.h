#ifndef DOWNLOADER1_H
#define DOWNLOADER1_H

#include <QObject>
#include <string>
#include <filesystem>
#include <QtNetwork>
#include "confighandler.h"
#include "stage.h"
#include "stage1.h"
#include "runnable.h"

class Downloader1 : public Runnable
{
public:
    Downloader1(ConfigHandler *);

private:
    std::string filenameRelPath;
    std::string datasetType;

    int download();

    quint64 getTgzMax();
    quint64 getTgzSize();

public slots:
    void run();
};

#endif // DOWNLOADER1_H
