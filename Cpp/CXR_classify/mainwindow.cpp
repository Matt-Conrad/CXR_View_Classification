#include "mainwindow.h"

MainWindow::MainWindow(QWidget *parent) : QMainWindow(parent)
{
    fillWindow();
    show();
}

void MainWindow::fillWindow()
{
    centralWidget = new QWidget(this);

    // Create all widgets
    QLabel * msgBox = new QLabel("Welcome to the CXR Classification Application");
    QProgressBar * proBar = new QProgressBar;
//    QPushButton * downloadBtn = new QPushButton("Download");
    QPushButton * downloadBtn = new DownloadButton("Download");
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

void MainWindow::updateText(QString text)
{
    centralWidget->findChild<QLabel *>("msgBox")->setText(text);
}

void MainWindow::updateProBar(uint64_t value)
{
    centralWidget->findChild<QProgressBar *>("proBar")->setValue(value);
}

void MainWindow::stage1_ui()
{
    centralWidget->findChild<QPushButton *>("downloadBtn")->setDisabled(false);
    centralWidget->findChild<QPushButton *>("unpackBtn")->setDisabled(true);
    centralWidget->findChild<QPushButton *>("storeBtn")->setDisabled(true);
    centralWidget->findChild<QPushButton *>("featuresBtn")->setDisabled(true);
    centralWidget->findChild<QPushButton *>("labelBtn")->setDisabled(true);
    centralWidget->findChild<QPushButton *>("classifyBtn")->setDisabled(true);
}

void MainWindow::stage2_ui()
{
    centralWidget->findChild<QPushButton *>("downloadBtn")->setDisabled(true);
    centralWidget->findChild<QPushButton *>("unpackBtn")->setDisabled(false);
    centralWidget->findChild<QPushButton *>("storeBtn")->setDisabled(true);
    centralWidget->findChild<QPushButton *>("featuresBtn")->setDisabled(true);
    centralWidget->findChild<QPushButton *>("labelBtn")->setDisabled(true);
    centralWidget->findChild<QPushButton *>("classifyBtn")->setDisabled(true);
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