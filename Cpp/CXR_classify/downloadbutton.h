#ifndef DOWNLOADBUTTON_H
#define DOWNLOADBUTTON_H

#include <QPushButton>
#include <QMainWindow>
#include <iostream>

class AppController;

class DownloadButton : public QPushButton
{
    Q_OBJECT
public:
    DownloadButton(const char * text, QMainWindow * window, AppController * controller);

private:
    AppController * controller;

private slots:
    void test();
};

#endif // DOWNLOADBUTTON_H
