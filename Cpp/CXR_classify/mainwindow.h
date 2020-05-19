#ifndef MAINAPPLICATION_H
#define MAINAPPLICATION_H

#include <QMainWindow>
#include <QWidget>
#include <QPushButton>
#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QGridLayout>
#include <QLabel>
#include <QProgressBar>

#include "unpackbutton.h"
#include "datasetdownloader.h"

class AppController;

class MainWindow : public QMainWindow
{
    Q_OBJECT
public:
    MainWindow(AppController * controller);

    void stage1_ui(DatasetDownloader * downloader);
    void stage2_ui();
    void stage3_ui();
    void stage4_ui();
    void stage5_ui();
    void stage6_ui();

private:
    AppController * controller;

    QWidget * centralWidget = nullptr;

    void fillWindow();

public slots:
    void updateText(QString text);
    void updateProBar(uint64_t value);

};

#endif // MAINAPPLICATION_H
