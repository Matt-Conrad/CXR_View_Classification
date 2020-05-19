#include "downloadbutton.h"
#include "appcontroller.h"

DownloadButton::DownloadButton(const char * text, QMainWindow * window, AppController * controller) : QPushButton(text, window)
{
    DownloadButton::controller = controller;
//    connect(this, SIGNAL (clicked()), controller->downloader, SLOT (getDataset()));
    connect(this, SIGNAL (clicked()), this, SLOT (downloadDataset()));
}


void DownloadButton::downloadDataset()
{
    QThread * thread = new QThread;
    Worker * worker = new Worker(controller);
    worker->moveToThread(thread);
    connect(thread, SIGNAL (started()), worker, SLOT (process()));
    connect(worker, SIGNAL (finished()), thread, SLOT (quit()));
    connect(worker, SIGNAL (finished()), worker, SLOT (deleteLater()));
    connect(thread, SIGNAL (finished()), thread, SLOT (deleteLater()));
    thread->start();
}

