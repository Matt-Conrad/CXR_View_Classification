#include "unpackbutton.h"
#include "appcontroller.h"

UnpackButton::UnpackButton(const char * text, QMainWindow * window, AppController * controller) : QPushButton(text, window)
{
    UnpackButton::controller = controller;
    connect(this, SIGNAL (clicked()), controller->downloader, SLOT (unpack()));
}

