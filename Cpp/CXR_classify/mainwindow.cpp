#include "mainwindow.h"
#include <appcontroller.h>

MainWindow::MainWindow(AppController * controller) : QMainWindow()
{
    MainWindow::controller = controller;
    fillWindow();
    show();
}

void MainWindow::fillWindow()
{
    centralWidget = new QWidget(this);

    // Create all widgets
    QLabel * msgBox = new QLabel("Welcome to the CXR Classification Application");
    QProgressBar * proBar = new QProgressBar;

    QPushButton * downloadBtn = new QPushButton("Download");
    QPushButton * unpackBtn = new QPushButton("Unpack");
    QPushButton * storeBtn = new QPushButton("Store Metadata");
    QPushButton * featuresBtn = new QPushButton("Calculate Features");
    QPushButton * labelBtn = new QPushButton("Label Images");
    QPushButton * classifyBtn = new QPushButton("Train Classifier");

    // Set object names to access them through the centralWidget
    msgBox->setObjectName("msgBox");
    proBar->setObjectName("proBar");
    downloadBtn->setObjectName("downloadBtn");
    unpackBtn->setObjectName("unpackBtn");
    storeBtn->setObjectName("storeBtn");
    featuresBtn->setObjectName("featuresBtn");
    labelBtn->setObjectName("labelBtn");
    classifyBtn->setObjectName("classifyBtn");

    // Add widgets to layout
    QGridLayout * layout = new QGridLayout;
    layout->addWidget(msgBox, 0, 0, 1, 3);
    layout->addWidget(proBar, 1, 0, 1, 3);
    layout->addWidget(downloadBtn, 2, 0);
    layout->addWidget(unpackBtn, 2, 1);
    layout->addWidget(storeBtn, 2, 2);
    layout->addWidget(featuresBtn, 3, 0);
    layout->addWidget(labelBtn, 3, 1);
    layout->addWidget(classifyBtn, 3, 2);

    // Set layout
    centralWidget->setLayout(layout);
    setCentralWidget(centralWidget);
}

void MainWindow::startDashboard(QString text, quint64 proBarMin, quint64 proBarMax) {
    centralWidget->findChild<QLabel *>("msgBox")->setText(text);
    centralWidget->findChild<QProgressBar *>("proBar")->setMinimum(proBarMin);
    centralWidget->findChild<QProgressBar *>("proBar")->setMaximum(proBarMax);
}


void MainWindow::updateProgressBar(quint64 value) {
    centralWidget->findChild<QProgressBar *>("proBar")->setValue(value);
//    while (getTgzSize() < getTgzMax()) {
//        centralWidget->findChild<QProgressBar *>("proBar")->setValue(getTgzSize());
//        std::this_thread::sleep_for(std::chrono::seconds(1));
//    }
//    centralWidget->findChild<QProgressBar *>("proBar")->setValue(getTgzSize());
//    centralWidget->findChild<QLabel *>("msgBox")->setText("Image download complete");

//    centralWidget->findChild<QPushButton *>("downloadBtn")->setDisabled(true);
//    centralWidget->findChild<QPushButton *>("unpackBtn")->setDisabled(false);
//    centralWidget->findChild<QPushButton *>("storeBtn")->setDisabled(true);
//    centralWidget->findChild<QPushButton *>("featuresBtn")->setDisabled(true);
//    centralWidget->findChild<QPushButton *>("labelBtn")->setDisabled(true);
//    centralWidget->findChild<QPushButton *>("classifyBtn")->setDisabled(true);
}

void MainWindow::stage1_ui()
{
    centralWidget->findChild<QPushButton *>("downloadBtn")->setDisabled(false);
    centralWidget->findChild<QPushButton *>("unpackBtn")->setDisabled(true);
    centralWidget->findChild<QPushButton *>("storeBtn")->setDisabled(true);
    centralWidget->findChild<QPushButton *>("featuresBtn")->setDisabled(true);
    centralWidget->findChild<QPushButton *>("labelBtn")->setDisabled(true);
    centralWidget->findChild<QPushButton *>("classifyBtn")->setDisabled(true);

    QThread * downloadThread = new QThread;
    controller->downloader->moveToThread(downloadThread);
    connect(centralWidget->findChild<QPushButton *>("downloadBtn"), SIGNAL (clicked()), downloadThread, SLOT (start()));

    QThread * downloadUpdaterThread = new QThread;
    controller->downloadUpdater->moveToThread(downloadUpdaterThread);
    connect(centralWidget->findChild<QPushButton *>("downloadBtn"), SIGNAL (clicked()), downloadUpdaterThread, SLOT (start()));

    connect(downloadThread, SIGNAL (started()), controller->downloader, SLOT (getDataset()));
    connect(downloadUpdaterThread, SIGNAL (started()), controller->downloadUpdater, SLOT (updateProgressBar()));

    connect(controller->downloader, SIGNAL (requestStartDashboard(QString, quint64, quint64)), this, SLOT (startDashboard(QString, quint64, quint64)));
    connect(controller->downloadUpdater, SIGNAL (attemptUpdateProBar(quint64)), this, SLOT (updateProgressBar(quint64)));

    connect(controller->downloader, SIGNAL (finished()), downloadThread, SLOT (quit()));
    connect(controller->downloadUpdater, SIGNAL (finished()), downloadUpdaterThread, SLOT (quit()));

    connect(controller->downloader, SIGNAL (finished()), controller->downloader, SLOT (deleteLater()));
    connect(downloadThread, SIGNAL (finished()), downloadThread, SLOT (deleteLater()));
    connect(controller->downloadUpdater, SIGNAL (finished()), controller->downloadUpdater, SLOT (deleteLater()));
    connect(downloadUpdaterThread, SIGNAL (finished()), downloadUpdaterThread, SLOT (deleteLater()));
}

void MainWindow::stage2_ui(Unpacker * unpacker)
{
    centralWidget->findChild<QPushButton *>("downloadBtn")->setDisabled(true);
    centralWidget->findChild<QPushButton *>("unpackBtn")->setDisabled(false);
    centralWidget->findChild<QPushButton *>("storeBtn")->setDisabled(true);
    centralWidget->findChild<QPushButton *>("featuresBtn")->setDisabled(true);
    centralWidget->findChild<QPushButton *>("labelBtn")->setDisabled(true);
    centralWidget->findChild<QPushButton *>("classifyBtn")->setDisabled(true);

    QThread * unpackThread = new QThread;
    unpacker->moveToThread(unpackThread);
    connect(centralWidget->findChild<QPushButton *>("unpackBtn"), SIGNAL (clicked()), unpackThread, SLOT (start()));
    connect(unpackThread, SIGNAL (started()), unpacker, SLOT (unpack()));
    connect(unpacker, SIGNAL (finished()), unpackThread, SLOT (quit()));
    connect(unpacker, SIGNAL (finished()), unpacker, SLOT (deleteLater()));
    connect(unpackThread, SIGNAL (finished()), unpackThread, SLOT (deleteLater()));
}

void MainWindow::stage3_ui()
{
    centralWidget->findChild<QPushButton *>("downloadBtn")->setDisabled(true);
    centralWidget->findChild<QPushButton *>("unpackBtn")->setDisabled(true);
    centralWidget->findChild<QPushButton *>("storeBtn")->setDisabled(false);
    centralWidget->findChild<QPushButton *>("featuresBtn")->setDisabled(true);
    centralWidget->findChild<QPushButton *>("labelBtn")->setDisabled(true);
    centralWidget->findChild<QPushButton *>("classifyBtn")->setDisabled(true);
}

void MainWindow::stage4_ui()
{
    centralWidget->findChild<QPushButton *>("downloadBtn")->setDisabled(true);
    centralWidget->findChild<QPushButton *>("unpackBtn")->setDisabled(true);
    centralWidget->findChild<QPushButton *>("storeBtn")->setDisabled(true);
    centralWidget->findChild<QPushButton *>("featuresBtn")->setDisabled(false);
    centralWidget->findChild<QPushButton *>("labelBtn")->setDisabled(true);
    centralWidget->findChild<QPushButton *>("classifyBtn")->setDisabled(true);
}

void MainWindow::stage5_ui()
{
    centralWidget->findChild<QPushButton *>("downloadBtn")->setDisabled(true);
    centralWidget->findChild<QPushButton *>("unpackBtn")->setDisabled(true);
    centralWidget->findChild<QPushButton *>("storeBtn")->setDisabled(true);
    centralWidget->findChild<QPushButton *>("featuresBtn")->setDisabled(true);
    centralWidget->findChild<QPushButton *>("labelBtn")->setDisabled(false);
    centralWidget->findChild<QPushButton *>("classifyBtn")->setDisabled(true);
}

void MainWindow::stage6_ui()
{
    centralWidget->findChild<QPushButton *>("downloadBtn")->setDisabled(true);
    centralWidget->findChild<QPushButton *>("unpackBtn")->setDisabled(true);
    centralWidget->findChild<QPushButton *>("storeBtn")->setDisabled(true);
    centralWidget->findChild<QPushButton *>("featuresBtn")->setDisabled(true);
    centralWidget->findChild<QPushButton *>("labelBtn")->setDisabled(true);
    centralWidget->findChild<QPushButton *>("classifyBtn")->setDisabled(false);
}
