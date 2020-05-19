#ifndef DOWNLOADBUTTON_H
#define DOWNLOADBUTTON_H

#include <QPushButton>
#include <QMainWindow>
#include <QObject>
#include <iostream>
#include "worker.h"

class AppController;

class DownloadButton : public QPushButton
{
    Q_OBJECT
public:
    DownloadButton(const char * text, QMainWindow * window, AppController * controller);
    AppController * controller;

private slots:
    void downloadDataset();
};

#endif // DOWNLOADBUTTON_H
