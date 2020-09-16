#include "downloadstage.h"

DownloadStage::DownloadStage(ConfigHandler * configHandler) : Stage1()
{
    downloader = new Downloader(configHandler);
}

void DownloadStage::download()
{
    threadpool->start(downloader);
}
