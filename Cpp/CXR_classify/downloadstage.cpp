#include "downloadstage.h"


DownloadStage::DownloadStage(ConfigHandler * configHandler) : Stage1()
{
    DownloadStage::downloader = new Downloader1(configHandler);
}

void DownloadStage::download()
{
    threadpool->start(downloader);

}
