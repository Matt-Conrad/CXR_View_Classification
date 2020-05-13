#include "mainwindow.h"

MainWindow::MainWindow(QWidget *parent) : QMainWindow(parent)
{
    fillWindow();
    show();
}

void MainWindow::fillWindow()
{
    centralWidget = new QWidget(this);

    QVBoxLayout * fullLayout = new QVBoxLayout(centralWidget);

    QVBoxLayout * feedbackDashboard = new QVBoxLayout;
    QLabel * msgBox = new QLabel("Welcome to the CXR Classification Application");
    QProgressBar * proBar = new QProgressBar;
    feedbackDashboard->addWidget(msgBox);
    feedbackDashboard->addWidget(proBar);

    QHBoxLayout * upperButtons = new QHBoxLayout;
    QHBoxLayout * lowerButtons = new QHBoxLayout;

    QPushButton * button1 = new QPushButton("Download");
    upperButtons->addWidget(button1);

    QPushButton * button2 = new QPushButton("Unpack");
    upperButtons->addWidget(button2);

    QPushButton * button3 = new QPushButton("Store Metadata");
    upperButtons->addWidget(button3);

    QPushButton * button4 = new QPushButton("Calculate Features");
    lowerButtons->addWidget(button4);

    QPushButton * button5 = new QPushButton("Label Images");
    lowerButtons->addWidget(button5);

    QPushButton * button6 = new QPushButton("Train Classifier");
    lowerButtons->addWidget(button6);

    fullLayout->addLayout(feedbackDashboard);
    fullLayout->addLayout(upperButtons);
    fullLayout->addLayout(lowerButtons);

    setCentralWidget(centralWidget);
}
