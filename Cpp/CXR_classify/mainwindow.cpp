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
    QPushButton * trainBtn = new QPushButton("Train Classifier");

    downloadBtn->setObjectName("downloadBtn");
    unpackBtn->setObjectName("unpackBtn");
    storeBtn->setObjectName("storeBtn");
    featureBtn->setObjectName("featureBtn");
    labelBtn->setObjectName("labelBtn");
    trainBtn->setObjectName("trainBtn");

    QGridLayout * stagesLayout = new QGridLayout();
    stagesLayout->addWidget(downloadBtn, 1, 0);
    stagesLayout->addWidget(unpackBtn, 1, 1);
    stagesLayout->addWidget(storeBtn, 1, 2);
    stagesLayout->addWidget(featureBtn, 2, 0);
    stagesLayout->addWidget(labelBtn, 2, 1);
    stagesLayout->addWidget(trainBtn, 2, 2);

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

    connect(frontalBtn, SIGNAL (clicked()), controller->labelStage->labeler, SLOT (frontal()));
    connect(lateralBtn, SIGNAL (clicked()), controller->labelStage->labeler, SLOT (lateral()));

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
        trainStageUi();
    } else if (controller->dbHandler->tableExists(controller->configHandler->getTableName("features"))) {
        labelStageUi();
    } else if (controller->dbHandler->tableExists(controller->configHandler->getTableName("metadata"))) {
        calcFeatStageUi();
    } else if (std::filesystem::exists(folderRelPath)) {
        storeStageUi();
    } else if (std::filesystem::exists(controller->configHandler->getTgzFilename())) {
        unpackStageUi();
    } else {
        downloadStageUi();
    }
}

void MainWindow::downloadStageUi()
{
    disableAllStageButtons();
    enableStageButton(0);

    connect(mainWidget->findChild<QPushButton *>("downloadBtn"), SIGNAL (clicked()), controller->downloadStage, SLOT (download()));
    connectToDashboard(controller->downloadStage->downloader->signalOptions);
    connect(controller->downloadStage->downloader->signalOptions, SIGNAL (finished()), this, SLOT(unpackStageUi()));
}

void MainWindow::unpackStageUi()
{
    disableAllStageButtons();
    enableStageButton(1);

    connect(mainWidget->findChild<QPushButton *>("unpackBtn"), SIGNAL (clicked()), controller->unpackStage, SLOT (unpack()));
    connectToDashboard(controller->unpackStage->unpacker->signalOptions);
    connect(controller->unpackStage->unpacker->signalOptions, SIGNAL (finished()), this, SLOT(storeStageUi()));
}

void MainWindow::storeStageUi()
{
    disableAllStageButtons();
    enableStageButton(2);

    connect(mainWidget->findChild<QPushButton *>("storeBtn"), SIGNAL (clicked()), controller->storeStage, SLOT (store()));
    connectToDashboard(controller->storeStage->storer->signalOptions);
    connect(controller->storeStage->storer->signalOptions, SIGNAL (finished()), this, SLOT(calcFeatStageUi()));
}

void MainWindow::calcFeatStageUi()
{
    disableAllStageButtons();
    enableStageButton(3);

    connect(mainWidget->findChild<QPushButton *>("featureBtn"), SIGNAL (clicked()), controller->featureCalculatorStage, SLOT (calculateFeatures()));
    connectToDashboard(controller->featureCalculatorStage->featureCalculator->signalOptions);
    connect(controller->featureCalculatorStage->featureCalculator->signalOptions, SIGNAL (finished()), this, SLOT(labelStageUi()));
}

void MainWindow::labelStageUi()
{
    disableAllStageButtons();
    enableStageButton(4);

    connectToDashboard(controller->labelStage->labeler->signalOptions);

    if (controller->configHandler->getDatasetType() == "subset") {
        connect(mainWidget->findChild<QPushButton *>("labelBtn"), SIGNAL (clicked()), controller->labelStage, SLOT (label()));

        connect(mainWidget->findChild<QPushButton *>("labelBtn"), SIGNAL (clicked()), this, SLOT (secondPage()));
        connect(controller->labelStage->labeler->signalOptions, SIGNAL (finished()), this, SLOT (firstPage()));
    }

    connect(controller->labelStage->labeler->signalOptions, SIGNAL (finished()), this, SLOT (trainStageUi()));
}

void MainWindow::trainStageUi()
{
    widgetStack->setFixedSize(widgetStack->currentWidget()->layout()->sizeHint());
    setFixedSize(centralWidget()->layout()->sizeHint());

    disableAllStageButtons();
    enableStageButton(5);

    connect(mainWidget->findChild<QPushButton *>("trainBtn"), SIGNAL (clicked()), controller->trainStage, SLOT (train()));
    connectToDashboard(controller->trainStage->trainer->signalOptions);
}

void MainWindow::firstPage()
{
    widgetStack->setCurrentIndex(0);
}

void MainWindow::secondPage()
{
    widgetStack->setCurrentIndex(1);
}

void MainWindow::connectToDashboard(Signals * sigs)
{
    connect(sigs, SIGNAL (attemptUpdateProBarBounds(quint64, quint64)), this, SLOT (updateProBarBounds(quint64, quint64)));
    connect(sigs, SIGNAL (attemptUpdateProBarValue(quint64)), this, SLOT (updateProBarValue(quint64)));
    connect(sigs, SIGNAL (attemptUpdateText(QString)), this, SLOT (updateText(QString)));
    connect(sigs, SIGNAL (attemptUpdateImage(QPixmap)), this, SLOT (updateImage(QPixmap)));
}

void MainWindow::disableAllStageButtons()
{
    mainWidget->findChild<QPushButton *>("downloadBtn")->setDisabled(true);
    mainWidget->findChild<QPushButton *>("unpackBtn")->setDisabled(true);
    mainWidget->findChild<QPushButton *>("storeBtn")->setDisabled(true);
    mainWidget->findChild<QPushButton *>("featureBtn")->setDisabled(true);
    mainWidget->findChild<QPushButton *>("labelBtn")->setDisabled(true);
    mainWidget->findChild<QPushButton *>("trainBtn")->setDisabled(true);
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

void MainWindow::updateImage(QPixmap pixmap) {
    widgetStack->findChild<QLabel *>("image")->setPixmap(pixmap);
}

