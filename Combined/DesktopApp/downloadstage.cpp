#include "downloadstage.h"

DownloadStage::DownloadStage(ConfigHandler * configHandler) : Stage()
{
    downloader = new Downloader(configHandler);
}

void DownloadStage::download()
{
    threadpool->start(downloader);
}
