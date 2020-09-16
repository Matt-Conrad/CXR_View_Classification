#ifndef DOWNLOADSTAGE_H
#define DOWNLOADSTAGE_H

#include <QObject>
#include <string>
#include <filesystem>
#include <QtNetwork>
#include "confighandler.h"
#include "stage.h"
#include "stage1.h"
#include "runnable.h"
#include "downloader1.h"

class DownloadStage : public Stage1
{
    Q_OBJECT
public:
    DownloadStage(ConfigHandler *);
    Downloader1 * downloader;


public slots:
    void download();
};

#endif // DOWNLOADSTAGE_H
