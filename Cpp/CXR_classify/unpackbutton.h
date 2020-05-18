#ifndef UNPACKBUTTON_H
#define UNPACKBUTTON_H


#include <QPushButton>
#include <QMainWindow>
#include <iostream>

class AppController;

class UnpackButton : public QPushButton
{
    Q_OBJECT
public:
    UnpackButton(const char * text, QMainWindow * window, AppController * controller);

private:
    AppController * controller;
};

#endif // UNPACKBUTTON_H
