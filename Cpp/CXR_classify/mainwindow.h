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
#include <filesystem>

#include "downloader.h"
#include "downloadupdater.h"
#include "unpacker.h"

class AppController;

class MainWindow : public QMainWindow
{
    Q_OBJECT
public:
    MainWindow(AppController * controller);

    void stage1_ui();
    void stage2_ui(Unpacker * unpacker);
    void stage3_ui();
    void stage4_ui();
    void stage5_ui();
    void stage6_ui();

private:
    AppController * controller;

    QWidget * centralWidget = nullptr;

    void fillWindow();

public slots:
    void startDashboard(QString, quint64, quint64);
    void updateProgressBar(quint64);

};

#endif // MAINAPPLICATION_H
