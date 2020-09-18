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
    DownloadStage * downloadStage = new DownloadStage(configHandler); // MAKE SURE TO DELETE THIS AFTERWARD

    disableAllStageButtons();
    enableStageButton(0);

    connect(mainWidget->findChild<QPushButton *>("downloadBtn"), SIGNAL (clicked()), downloadStage, SLOT (download()));
    connectToDashboard(downloadStage->downloader);
    connect(downloadStage->downloader, SIGNAL (finished()), this, SLOT(unpackStageUi()));
}

void MainWindow::unpackStageUi()
{
    UnpackStage * unpackStage = new UnpackStage(configHandler); // MAKE SURE TO DELETE THIS AFTERWARD

    disableAllStageButtons();
    enableStageButton(1);

    connect(mainWidget->findChild<QPushButton *>("unpackBtn"), SIGNAL (clicked()), unpackStage, SLOT (unpack()));
    connectToDashboard(unpackStage->unpacker);
    connect(unpackStage->unpacker, SIGNAL (finished()), this, SLOT(storeStageUi()));
}

void MainWindow::storeStageUi()
{
    StoreStage * storeStage = new StoreStage(configHandler, dbHandler); // MAKE SURE TO DELETE THIS AFTERWARD

    disableAllStageButtons();
    enableStageButton(2);

    connect(mainWidget->findChild<QPushButton *>("storeBtn"), SIGNAL (clicked()), storeStage, SLOT (store()));
    connectToDashboard(storeStage->storer);
    connect(storeStage->storer, SIGNAL (finished()), this, SLOT(calcFeatStageUi()));
}

void MainWindow::calcFeatStageUi()
{
    FeatureCalculatorStage * featCalcStage = new FeatureCalculatorStage(configHandler, dbHandler); // MAKE SURE TO DELETE THIS AFTERWARD

    disableAllStageButtons();
    enableStageButton(3);

    connect(mainWidget->findChild<QPushButton *>("featureBtn"), SIGNAL (clicked()), featCalcStage, SLOT (calculateFeatures()));
    connectToDashboard(featCalcStage->featureCalculator);
    connect(featCalcStage->featureCalculator, SIGNAL (finished()), this, SLOT(labelStageUi()));
}

void MainWindow::labelStageUi()
{
    LabelStage * labelStage = new LabelStage(configHandler, dbHandler); // MAKE SURE TO DELETE THIS AFTERWARD

    disableAllStageButtons();
    enableStageButton(4);

    connect(mainWidget->findChild<QPushButton *>("labelBtn"), SIGNAL (clicked()), labelStage, SLOT (label()));

    if (configHandler->getDatasetType() == "subset") {
        connectToDashboard(labelStage->labeler);

        connect(widgetStack->findChild<QPushButton *>("frontalBtn"), SIGNAL (clicked()), labelStage->labeler, SLOT (frontal()));
        connect(widgetStack->findChild<QPushButton *>("lateralBtn"), SIGNAL (clicked()), labelStage->labeler, SLOT (lateral()));

        connect(mainWidget->findChild<QPushButton *>("labelBtn"), SIGNAL (clicked()), this, SLOT (secondPage()));
        connect(labelStage->labeler, SIGNAL (finished()), this, SLOT (firstPage()));
        connect(labelStage->labeler, SIGNAL (finished()), this, SLOT (trainStageUi()));
    } else {
        connectToDashboard(labelStage->labeler);
        connect(labelStage->labeler, SIGNAL (finished()), this, SLOT (trainStageUi()));
    }
}

void MainWindow::trainStageUi()
{
    TrainStage * trainStage = new TrainStage(configHandler, dbHandler); // MAKE SURE TO DELETE THIS AFTERWARD

    widgetStack->setFixedSize(widgetStack->currentWidget()->layout()->sizeHint());
    setFixedSize(centralWidget()->layout()->sizeHint());

    disableAllStageButtons();
    enableStageButton(5);

    connect(mainWidget->findChild<QPushButton *>("trainBtn"), SIGNAL (clicked()), trainStage, SLOT (train()));
    connectToDashboard(trainStage->trainer);
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

