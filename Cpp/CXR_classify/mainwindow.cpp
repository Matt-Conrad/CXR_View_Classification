#include "mainwindow.h"
#include <appcontroller.h>

MainWindow::MainWindow(AppController * controller) : QMainWindow()
{
    MainWindow::controller = controller;
    fillWindow();
    initGuiState();
    show();
}

void MainWindow::fillWindow()
{
    // Create widget for the dashboard
    QWidget * dashboardWidget = new QWidget();

    QLabel * msgBox = new QLabel("Welcome to the CXR Classification Application");
    QProgressBar * proBar = new QProgressBar;

    msgBox->setObjectName("msgBox");
    proBar->setObjectName("proBar");

    QGridLayout * dashboardLayout = new QGridLayout();
    dashboardLayout->addWidget(msgBox, 1, 0, 1, 3);
    dashboardLayout->addWidget(proBar, 2, 0, 1, 3);

    dashboardWidget->setLayout(dashboardLayout);

    // Create widget for the stage buttons
    QWidget * stagesWidget = new QWidget();

    QPushButton * downloadBtn = new QPushButton("Download");
    QPushButton * unpackBtn = new QPushButton("Unpack");
    QPushButton * storeBtn = new QPushButton("Store Metadata");
    QPushButton * featureBtn = new QPushButton("Calculate Features");
    QPushButton * labelBtn = new QPushButton("Label Images");
    QPushButton * classifyBtn = new QPushButton("Train Classifier");

    downloadBtn->setObjectName("downloadBtn");
    unpackBtn->setObjectName("unpackBtn");
    storeBtn->setObjectName("storeBtn");
    featureBtn->setObjectName("featureBtn");
    labelBtn->setObjectName("labelBtn");
    classifyBtn->setObjectName("classifyBtn");

    QGridLayout * stagesLayout = new QGridLayout();
    stagesLayout->addWidget(downloadBtn, 1, 0);
    stagesLayout->addWidget(unpackBtn, 1, 1);
    stagesLayout->addWidget(storeBtn, 1, 2);
    stagesLayout->addWidget(featureBtn, 2, 0);
    stagesLayout->addWidget(labelBtn, 2, 1);
    stagesLayout->addWidget(classifyBtn, 2, 2);

    stagesWidget->setLayout(stagesLayout);

    // Create widget for the labeler
    QWidget * labelerWidget = new QWidget();

    QLabel * image = new QLabel();
    image->setAlignment(Qt::AlignCenter);
    QPushButton * frontalBtn = new QPushButton("Frontal");
    QPushButton * lateralBtn = new QPushButton("Lateral");

    image->setObjectName("image");
    frontalBtn->setObjectName("frontalBtn");
    lateralBtn->setObjectName("lateralBtn");

    QGridLayout * labelLayout = new QGridLayout();
    labelLayout->addWidget(image, 1, 0, 1, 2);
    labelLayout->addWidget(frontalBtn, 2, 0);
    labelLayout->addWidget(lateralBtn, 2, 1);

    labelerWidget->setLayout(labelLayout);

    // Set up widget stack
    widgetStack = new QStackedWidget();
    widgetStack->addWidget(stagesWidget);
    widgetStack->addWidget(labelerWidget);

    // Full stack
    mainWidget = new QWidget(this);
    QVBoxLayout * mainLayout = new QVBoxLayout();
    mainLayout->addWidget(dashboardWidget);
    mainLayout->addWidget(widgetStack);
    mainWidget->setLayout(mainLayout);

    setCentralWidget(mainWidget);
}

void MainWindow::initGuiState()
{
    setWindowIcon(QIcon("../../miscellaneous/icon.jpg"));

    std::string folderRelPath = "./" + controller->configHandler->getDatasetName();

    if (controller->dbHandler->tableExists(controller->configHandler->getTableName("label"))) {
        stage6_ui();
    } else if (controller->dbHandler->tableExists(controller->configHandler->getTableName("features"))) {
        stage5_ui();
    } else if (controller->dbHandler->tableExists(controller->configHandler->getTableName("metadata"))) {
        stage4_ui();
    } else if (std::filesystem::exists(folderRelPath)) {
        stage3_ui();
    } else if (std::filesystem::exists(controller->configHandler->getTgzFilename())) {
        stage2_ui();
    } else {
        stage1_ui();
    }
}

void MainWindow::stage1_ui()
{
    disableAllStageButtons();
    enableStageButton(0);

    connect(mainWidget->findChild<QPushButton *>("downloadBtn"), SIGNAL (clicked()), controller->downloadStage, SLOT (download()));
    connectToDashBoard1(controller->downloadStage->downloader->signalOptions);
    connect(controller->downloadStage->downloader->signalOptions, SIGNAL (finished()), this, SLOT(stage2_ui()));
}

void MainWindow::stage2_ui()
{
    disableAllStageButtons();
    enableStageButton(1);

    connect(mainWidget->findChild<QPushButton *>("unpackBtn"), SIGNAL (clicked()), controller->unpackStage, SLOT (unpack()));
    connectToDashBoard1(controller->unpackStage->unpacker->signalOptions);
    connect(controller->unpackStage->unpacker->signalOptions, SIGNAL (finished()), this, SLOT(stage3_ui()));
}

void MainWindow::stage3_ui()
{
    disableAllStageButtons();
    enableStageButton(2);

    connect(mainWidget->findChild<QPushButton *>("storeBtn"), SIGNAL (clicked()), controller->storeStage, SLOT (store()));
    connectToDashBoard1(controller->storeStage->storer->signalOptions);
    connect(controller->storeStage->storer->signalOptions, SIGNAL (finished()), this, SLOT(stage4_ui()));
}

void MainWindow::stage4_ui()
{
    disableAllStageButtons();
    enableStageButton(3);

    // Create a worker thread to download and a worker thread to update the GUI at the click of the button
    QThread * featCalcThread = new QThread;
    controller->featCalc->moveToThread(featCalcThread);
    connect(mainWidget->findChild<QPushButton *>("featureBtn"), SIGNAL (clicked()), featCalcThread, SLOT (start()));

    // Connect the threads to the functions of the classes in the threads
    connect(featCalcThread, SIGNAL (started()), controller->featCalc, SLOT (calculateFeatures()));

    // Connect the updater to the dashboard
    connectToDashBoard(controller->featCalc);

    // When functions in the threads finished, quit the thread, delete the objects in the threads, and delete the threads when able
    connect(controller->featCalc, SIGNAL (finished()), featCalcThread, SLOT (quit()));
    connect(controller->featCalc, SIGNAL (finished()), this, SLOT(stage5_ui()));
    connect(controller->featCalc, SIGNAL (finished()), controller->featCalc, SLOT (deleteLater()));
    connect(featCalcThread, SIGNAL (finished()), featCalcThread, SLOT (deleteLater()));
}

void MainWindow::stage5_ui()
{
    disableAllStageButtons();
    enableStageButton(4);

    if (controller->configHandler->getDatasetType() == "subset") {
        connect(mainWidget->findChild<QPushButton *>("labelBtn"), SIGNAL (clicked()), controller->labeler, SLOT (fillWindow()));
        connect(controller->labeler, SIGNAL (attemptUpdateText(QString)), this, SLOT (updateText(QString)));
        connect(controller->labeler, SIGNAL (finished()), this, SLOT(stage6_ui()));
        connect(controller->labeler, SIGNAL (finished()), controller->labeler, SLOT (deleteLater()));
    } else {
        connect(mainWidget->findChild<QPushButton *>("labelBtn"), SIGNAL (clicked()), controller->labelImporter, SLOT (importLabels()));
        connectToDashBoard(controller->labelImporter);
        connect(controller->labelImporter, SIGNAL (finished()), this, SLOT(stage6_ui()));
        connect(controller->labelImporter, SIGNAL (finished()), controller->labeler, SLOT (deleteLater()));
    }
}

void MainWindow::stage6_ui()
{
    disableAllStageButtons();
    enableStageButton(5);

    connect(mainWidget->findChild<QPushButton *>("classifyBtn"), SIGNAL (clicked()), controller->trainer, SLOT (trainClassifier()));
    connectToDashBoard(controller->trainer);
    connect(controller->trainer, SIGNAL (finished()), controller->labeler, SLOT (deleteLater()));
}

void MainWindow::connectToDashBoard(Stage * stage)
{
    connect(stage, SIGNAL (attemptUpdateProBarBounds(quint64, quint64)), this, SLOT (updateProBarBounds(quint64, quint64)));
    connect(stage, SIGNAL (attemptUpdateProBarValue(quint64)), this, SLOT (updateProBarValue(quint64)));
    connect(stage, SIGNAL (attemptUpdateText(QString)), this, SLOT (updateText(QString)));
}

void MainWindow::connectToDashBoard1(Signals * sigs)
{
    connect(sigs, SIGNAL (attemptUpdateProBarBounds(quint64, quint64)), this, SLOT (updateProBarBounds(quint64, quint64)));
    connect(sigs, SIGNAL (attemptUpdateProBarValue(quint64)), this, SLOT (updateProBarValue(quint64)));
    connect(sigs, SIGNAL (attemptUpdateText(QString)), this, SLOT (updateText(QString)));
}

void MainWindow::disableAllStageButtons()
{
    mainWidget->findChild<QPushButton *>("downloadBtn")->setDisabled(true);
    mainWidget->findChild<QPushButton *>("unpackBtn")->setDisabled(true);
    mainWidget->findChild<QPushButton *>("storeBtn")->setDisabled(true);
    mainWidget->findChild<QPushButton *>("featureBtn")->setDisabled(true);
    mainWidget->findChild<QPushButton *>("labelBtn")->setDisabled(true);
    mainWidget->findChild<QPushButton *>("classifyBtn")->setDisabled(true);
}

void MainWindow::enableStageButton(quint64 stageIndex)
{
    mainWidget->findChild<QPushButton *>(buttonsList[stageIndex])->setDisabled(false);
}

void MainWindow::updateText(QString text)
{
    mainWidget->findChild<QLabel *>("msgBox")->setText(text);
}

void MainWindow::updateProBarBounds(quint64 proBarMin, quint64 proBarMax)
{
    mainWidget->findChild<QProgressBar *>("proBar")->setMinimum(proBarMin);
    mainWidget->findChild<QProgressBar *>("proBar")->setMaximum(proBarMax);
}

void MainWindow::updateProBarValue(quint64 value) {
    mainWidget->findChild<QProgressBar *>("proBar")->setValue(value);
}
