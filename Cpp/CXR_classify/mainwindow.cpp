#include "mainwindow.h"

MainWindow::MainWindow() : QMainWindow()
{
    std::string url = c_sourceUrl.at(configHandler->getDatasetType());
    configHandler->setUrl(url);
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

    std::string folderRelPath = "./" + configHandler->getDatasetName();

    if (dbHandler->tableExists(configHandler->getTableName("label"))) {
        trainStageUi();
    } else if (dbHandler->tableExists(configHandler->getTableName("features"))) {
        labelStageUi();
    } else if (dbHandler->tableExists(configHandler->getTableName("metadata"))) {
        calcFeatStageUi();
    } else if (std::filesystem::exists(folderRelPath)) {
        storeStageUi();
    } else if (std::filesystem::exists(configHandler->getTgzFilename())) {
        unpackStageUi();
    } else {
        downloadStageUi();
    }
}

void MainWindow::downloadStageUi()
{
    currentStage = new DownloadStage(configHandler); // MAKE SURE TO DELETE THIS AFTERWARD

    disableAllStageButtons();
    enableStageButton(0);

    connect(mainWidget->findChild<QPushButton *>("downloadBtn"), SIGNAL (clicked()), static_cast<DownloadStage *>(currentStage), SLOT (download()));
    connectToDashboard(static_cast<DownloadStage *>(currentStage)->downloader);
    connect(static_cast<DownloadStage *>(currentStage)->downloader, SIGNAL (finished()), this, SLOT(clearCurrentStage()));
    connect(static_cast<DownloadStage *>(currentStage)->downloader, SIGNAL (finished()), this, SLOT(unpackStageUi()));
}

void MainWindow::unpackStageUi()
{
    currentStage = new UnpackStage(configHandler); // MAKE SURE TO DELETE THIS AFTERWARD

    disableAllStageButtons();
    enableStageButton(1);

    connect(mainWidget->findChild<QPushButton *>("unpackBtn"), SIGNAL (clicked()), static_cast<UnpackStage *>(currentStage), SLOT (unpack()));
    connectToDashboard(static_cast<UnpackStage *>(currentStage)->unpacker);
    connect(static_cast<DownloadStage *>(currentStage)->downloader, SIGNAL (finished()), this, SLOT(clearCurrentStage()));
    connect(static_cast<UnpackStage *>(currentStage)->unpacker, SIGNAL (finished()), this, SLOT(storeStageUi()));
}

void MainWindow::storeStageUi()
{
    currentStage = new StoreStage(configHandler, dbHandler); // MAKE SURE TO DELETE THIS AFTERWARD

    disableAllStageButtons();
    enableStageButton(2);

    connect(mainWidget->findChild<QPushButton *>("storeBtn"), SIGNAL (clicked()), static_cast<StoreStage *>(currentStage), SLOT (store()));
    connectToDashboard(static_cast<StoreStage *>(currentStage)->storer);
    connect(static_cast<DownloadStage *>(currentStage)->downloader, SIGNAL (finished()), this, SLOT(clearCurrentStage()));
    connect(static_cast<StoreStage *>(currentStage)->storer, SIGNAL (finished()), this, SLOT(calcFeatStageUi()));
}

void MainWindow::calcFeatStageUi()
{
    currentStage = new FeatureCalculatorStage(configHandler, dbHandler); // MAKE SURE TO DELETE THIS AFTERWARD

    disableAllStageButtons();
    enableStageButton(3);

    connect(mainWidget->findChild<QPushButton *>("featureBtn"), SIGNAL (clicked()), static_cast<FeatureCalculatorStage *>(currentStage), SLOT (calculateFeatures()));
    connectToDashboard(static_cast<FeatureCalculatorStage *>(currentStage)->featureCalculator);
    connect(static_cast<DownloadStage *>(currentStage)->downloader, SIGNAL (finished()), this, SLOT(clearCurrentStage()));
    connect(static_cast<FeatureCalculatorStage *>(currentStage)->featureCalculator, SIGNAL (finished()), this, SLOT(labelStageUi()));
}

void MainWindow::labelStageUi()
{
    currentStage = new LabelStage(configHandler, dbHandler); // MAKE SURE TO DELETE THIS AFTERWARD

    disableAllStageButtons();
    enableStageButton(4);

    connect(mainWidget->findChild<QPushButton *>("labelBtn"), SIGNAL (clicked()), static_cast<LabelStage *>(currentStage), SLOT (label()));

    if (configHandler->getDatasetType() == "subset") {
        connectToDashboard(static_cast<LabelStage *>(currentStage)->labeler);

        connect(widgetStack->findChild<QPushButton *>("frontalBtn"), SIGNAL (clicked()), static_cast<LabelStage *>(currentStage)->labeler, SLOT (frontal()));
        connect(widgetStack->findChild<QPushButton *>("lateralBtn"), SIGNAL (clicked()), static_cast<LabelStage *>(currentStage)->labeler, SLOT (lateral()));

        connect(mainWidget->findChild<QPushButton *>("labelBtn"), SIGNAL (clicked()), this, SLOT (secondPage()));
        connect(static_cast<LabelStage *>(currentStage)->labeler, SIGNAL (finished()), this, SLOT (firstPage()));
        connect(static_cast<DownloadStage *>(currentStage)->downloader, SIGNAL (finished()), this, SLOT(clearCurrentStage()));
        connect(static_cast<LabelStage *>(currentStage)->labeler, SIGNAL (finished()), this, SLOT (trainStageUi()));
    } else {
        connectToDashboard(static_cast<LabelStage *>(currentStage)->labeler);
        connect(static_cast<DownloadStage *>(currentStage)->downloader, SIGNAL (finished()), this, SLOT(clearCurrentStage()));
        connect(static_cast<LabelStage *>(currentStage)->labeler, SIGNAL (finished()), this, SLOT (trainStageUi()));
    }
}

void MainWindow::trainStageUi()
{
    currentStage = new TrainStage(configHandler, dbHandler); // MAKE SURE TO DELETE THIS AFTERWARD

    widgetStack->setFixedSize(widgetStack->currentWidget()->layout()->sizeHint());
    setFixedSize(centralWidget()->layout()->sizeHint());

    disableAllStageButtons();
    enableStageButton(5);

    connect(mainWidget->findChild<QPushButton *>("trainBtn"), SIGNAL (clicked()), static_cast<TrainStage *>(currentStage), SLOT (train()));
    connectToDashboard(static_cast<TrainStage *>(currentStage)->trainer);
}

void MainWindow::clearCurrentStage()
{
    delete currentStage;
}

void MainWindow::firstPage()
{
    widgetStack->setCurrentIndex(0);
}

void MainWindow::secondPage()
{
    widgetStack->setCurrentIndex(1);
}

void MainWindow::connectToDashboard(Runnable * stage)
{
    connect(stage, SIGNAL (attemptUpdateProBarBounds(quint64, quint64)), this, SLOT (updateProBarBounds(quint64, quint64)));
    connect(stage, SIGNAL (attemptUpdateProBarValue(quint64)), this, SLOT (updateProBarValue(quint64)));
    connect(stage, SIGNAL (attemptUpdateText(QString)), this, SLOT (updateText(QString)));
    connect(stage, SIGNAL (attemptUpdateImage(QPixmap)), this, SLOT (updateImage(QPixmap)));
}

void MainWindow::disableAllStageButtons()
{
    uint8_t numOfButtons = sizeof(buttonsList)/sizeof(buttonsList[0]);
    for (uint8_t i = 0; i < numOfButtons; i++) {
        mainWidget->findChild<QPushButton *>(buttonsList[i])->setDisabled(true);
    }
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

