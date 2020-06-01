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

void MainWindow::updateText(QString text)
{
    centralWidget->findChild<QLabel *>("msgBox")->setText(text);
}

void MainWindow::updateProBarBounds(quint64 proBarMin, quint64 proBarMax)
{
    centralWidget->findChild<QProgressBar *>("proBar")->setMinimum(proBarMin);
    centralWidget->findChild<QProgressBar *>("proBar")->setMaximum(proBarMax);
}

void MainWindow::updateProBarValue(quint64 value) {
    centralWidget->findChild<QProgressBar *>("proBar")->setValue(value);
}

void MainWindow::stage1_ui()
{
    // Disable unused buttons
    centralWidget->findChild<QPushButton *>("downloadBtn")->setDisabled(false);
    centralWidget->findChild<QPushButton *>("unpackBtn")->setDisabled(true);
    centralWidget->findChild<QPushButton *>("storeBtn")->setDisabled(true);
    centralWidget->findChild<QPushButton *>("featuresBtn")->setDisabled(true);
    centralWidget->findChild<QPushButton *>("labelBtn")->setDisabled(true);
    centralWidget->findChild<QPushButton *>("classifyBtn")->setDisabled(true);

    // Create a worker thread to download and a worker thread to update the GUI at the click of the button
    QThread * downloadThread = new QThread;
    controller->downloader->moveToThread(downloadThread);
    connect(centralWidget->findChild<QPushButton *>("downloadBtn"), SIGNAL (clicked()), downloadThread, SLOT (start()));

    QThread * downloadUpdaterThread = new QThread;
    controller->downloadUpdater->moveToThread(downloadUpdaterThread);
    connect(centralWidget->findChild<QPushButton *>("downloadBtn"), SIGNAL (clicked()), downloadUpdaterThread, SLOT (start()));
\
    // Connect the threads to the functions of the classes in the threads
    connect(downloadThread, SIGNAL (started()), controller->downloader, SLOT (getDataset()));
    connect(downloadUpdaterThread, SIGNAL (started()), controller->downloadUpdater, SLOT (updateProgressBar()));

    // Connect the updater to the dashboard
    connect(controller->downloadUpdater, SIGNAL (attemptUpdateProBarBounds(quint64, quint64)), this, SLOT (updateProBarBounds(quint64, quint64)));
    connect(controller->downloadUpdater, SIGNAL (attemptUpdateProBarValue(quint64)), this, SLOT (updateProBarValue(quint64)));
    connect(controller->downloadUpdater, SIGNAL (attemptUpdateText(QString)), this, SLOT (updateText(QString)));

    // When functions in the threads finished, quit the thread, delete the objects in the threads, and delete the threads when able
    connect(controller->downloader, SIGNAL (finished()), downloadThread, SLOT (quit()));
    connect(controller->downloadUpdater, SIGNAL (finished()), downloadUpdaterThread, SLOT (quit()));
    connect(controller->downloadUpdater, SIGNAL (finished()), this, SLOT(stage2_ui()));
    connect(controller->downloader, SIGNAL (finished()), controller->downloader, SLOT (deleteLater()));
    connect(controller->downloadUpdater, SIGNAL (finished()), controller->downloadUpdater, SLOT (deleteLater()));
    connect(downloadThread, SIGNAL (finished()), downloadThread, SLOT (deleteLater()));
    connect(downloadUpdaterThread, SIGNAL (finished()), downloadUpdaterThread, SLOT (deleteLater()));
}

void MainWindow::stage2_ui()
{
    centralWidget->findChild<QPushButton *>("downloadBtn")->setDisabled(true);
    centralWidget->findChild<QPushButton *>("unpackBtn")->setDisabled(false);
    centralWidget->findChild<QPushButton *>("storeBtn")->setDisabled(true);
    centralWidget->findChild<QPushButton *>("featuresBtn")->setDisabled(true);
    centralWidget->findChild<QPushButton *>("labelBtn")->setDisabled(true);
    centralWidget->findChild<QPushButton *>("classifyBtn")->setDisabled(true);

    // Create a worker thread to download and a worker thread to update the GUI at the click of the button
    QThread * unpackThread = new QThread;
    controller->unpacker->moveToThread(unpackThread);
    connect(centralWidget->findChild<QPushButton *>("unpackBtn"), SIGNAL (clicked()), unpackThread, SLOT (start()));

    QThread * unpackUpdaterThread = new QThread;
    controller->unpackUpdater->moveToThread(unpackUpdaterThread);
    connect(centralWidget->findChild<QPushButton *>("unpackBtn"), SIGNAL (clicked()), unpackUpdaterThread, SLOT (start()));
\
    // Connect the threads to the functions of the classes in the threads
    connect(unpackThread, SIGNAL (started()), controller->unpacker, SLOT (unpack()));
    connect(unpackUpdaterThread, SIGNAL (started()), controller->unpackUpdater, SLOT (updateProgressBar()));

    // Connect the updater to the dashboard
    connect(controller->unpackUpdater, SIGNAL (attemptUpdateProBarBounds(quint64, quint64)), this, SLOT (updateProBarBounds(quint64, quint64)));
    connect(controller->unpackUpdater, SIGNAL (attemptUpdateProBarValue(quint64)), this, SLOT (updateProBarValue(quint64)));
    connect(controller->unpackUpdater, SIGNAL (attemptUpdateText(QString)), this, SLOT (updateText(QString)));

    // When functions in the threads finished, quit the thread, delete the objects in the threads, and delete the threads when able
    connect(controller->unpacker, SIGNAL (finished()), unpackThread, SLOT (quit()));
    connect(controller->unpackUpdater, SIGNAL (finished()), unpackUpdaterThread, SLOT (quit()));
    connect(controller->unpackUpdater, SIGNAL (finished()), this, SLOT(stage3_ui()));
    connect(controller->unpacker, SIGNAL (finished()), controller->unpacker, SLOT (deleteLater()));
    connect(controller->unpackUpdater, SIGNAL (finished()), controller->unpackUpdater, SLOT (deleteLater()));
    connect(unpackThread, SIGNAL (finished()), unpackThread, SLOT (deleteLater()));
    connect(unpackUpdaterThread, SIGNAL (finished()), unpackUpdaterThread, SLOT (deleteLater()));
}

void MainWindow::stage3_ui()
{
    centralWidget->findChild<QPushButton *>("downloadBtn")->setDisabled(true);
    centralWidget->findChild<QPushButton *>("unpackBtn")->setDisabled(true);
    centralWidget->findChild<QPushButton *>("storeBtn")->setDisabled(false);
    centralWidget->findChild<QPushButton *>("featuresBtn")->setDisabled(true);
    centralWidget->findChild<QPushButton *>("labelBtn")->setDisabled(true);
    centralWidget->findChild<QPushButton *>("classifyBtn")->setDisabled(true);

    // Create a worker thread to download and a worker thread to update the GUI at the click of the button
    QThread * storeThread = new QThread;
    controller->storer->moveToThread(storeThread);
    connect(centralWidget->findChild<QPushButton *>("storeBtn"), SIGNAL (clicked()), storeThread, SLOT (start()));

    QThread * storeUpdaterThread = new QThread;
    controller->storeUpdater->moveToThread(storeUpdaterThread);
    connect(centralWidget->findChild<QPushButton *>("storeBtn"), SIGNAL (clicked()), storeUpdaterThread, SLOT (start()));
\
    // Connect the threads to the functions of the classes in the threads
    connect(storeThread, SIGNAL (started()), controller->storer, SLOT (dicomToDb()));
    connect(storeUpdaterThread, SIGNAL (started()), controller->storeUpdater, SLOT (updateProgressBar()));

    // Connect the updater to the dashboard
    connect(controller->storeUpdater, SIGNAL (attemptUpdateProBarBounds(quint64, quint64)), this, SLOT (updateProBarBounds(quint64, quint64)));
    connect(controller->storeUpdater, SIGNAL (attemptUpdateProBarValue(quint64)), this, SLOT (updateProBarValue(quint64)));
    connect(controller->storeUpdater, SIGNAL (attemptUpdateText(QString)), this, SLOT (updateText(QString)));

    // When functions in the threads finished, quit the thread, delete the objects in the threads, and delete the threads when able
    connect(controller->storer, SIGNAL (finished()), storeThread, SLOT (quit()));
    connect(controller->storeUpdater, SIGNAL (finished()), storeUpdaterThread, SLOT (quit()));
    connect(controller->storeUpdater, SIGNAL (finished()), this, SLOT(stage4_ui()));
    connect(controller->storer, SIGNAL (finished()), controller->storer, SLOT (deleteLater()));
    connect(controller->storeUpdater, SIGNAL (finished()), controller->storeUpdater, SLOT (deleteLater()));
    connect(storeThread, SIGNAL (finished()), storeThread, SLOT (deleteLater()));
    connect(storeUpdaterThread, SIGNAL (finished()), storeUpdaterThread, SLOT (deleteLater()));
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
