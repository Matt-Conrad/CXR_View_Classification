#include "downloadbutton.h"

DownloadButton::DownloadButton(const char * text) : QPushButton(text)
{
    connect(this, SIGNAL (clicked()), this, SLOT (test()));
}

void DownloadButton::test()
{
    std::cout << "test" << std::endl;
}
