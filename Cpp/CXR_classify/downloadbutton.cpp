#include "downloadbutton.h"
#include "appcontroller.h"

DownloadButton::DownloadButton(const char * text, QMainWindow * window, AppController * controller) : QPushButton(text, window)
{
    DownloadButton::controller = controller;
    connect(this, SIGNAL (clicked()), controller->downloader, SLOT (getDataset()));
}

void DownloadButton::test()
{
    std::cout << "test" << std::endl;
}
