#ifndef DOWNLOADSTAGE_H
#define DOWNLOADSTAGE_H

#include <QObject>
#include "confighandler.h"
#include "stage1.h"
#include "downloader.h"

class DownloadStage : public Stage1
{
    Q_OBJECT
public:
    DownloadStage(ConfigHandler *);
    Downloader * downloader;

public slots:
    void download();
};

#endif // DOWNLOADSTAGE_H
