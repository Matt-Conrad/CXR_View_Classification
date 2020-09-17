#ifndef DOWNLOADSTAGE_H
#define DOWNLOADSTAGE_H

#include <QObject>
#include "confighandler.h"
#include "stage.h"
#include "downloader.h"

class DownloadStage : public Stage
{
    Q_OBJECT
public:
    DownloadStage(ConfigHandler *);
    Downloader * downloader;

public slots:
    void download();
};

#endif // DOWNLOADSTAGE_H
