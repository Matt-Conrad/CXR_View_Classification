#include "appcontroller.h"

AppController::AppController()
{
    std::string url = c_sourceUrl.at(configHandler->getDatasetType());
    configHandler->setUrl(url);

    initGuiState();
}

AppController::~AppController()
{
    configHandler->~ConfigHandler();
}

void AppController::initGuiState()
{
    mainWindow.setWindowIcon(QIcon("../../miscellaneous/icon.jpg"));

    std::string folderRelPath = "./" + configHandler->getDatasetName();

    connect(this, SIGNAL (initStage1()), &mainWindow, SLOT (stage1_ui()));
    connect(this, SIGNAL (initStage2()), &mainWindow, SLOT (stage2_ui()));
    connect(this, SIGNAL (initStage3()), &mainWindow, SLOT (stage3_ui()));
    connect(this, SIGNAL (initStage4()), &mainWindow, SLOT (stage4_ui()));
    connect(this, SIGNAL (initStage5()), &mainWindow, SLOT (stage5_ui()));
    connect(this, SIGNAL (initStage6()), &mainWindow, SLOT (stage6_ui()));


    if (dbHandler->tableExists(configHandler->getTableName("label"))) {
        emit initStage6();
    } else if (dbHandler->tableExists(configHandler->getTableName("features"))) {
        emit initStage5();
    } else if (dbHandler->tableExists(configHandler->getTableName("metadata"))) {
        emit initStage4();
    } else if (std::filesystem::exists(folderRelPath)) {
        emit initStage3();
    } else if (std::filesystem::exists(configHandler->getTgzFilename())) {
        emit initStage2();
    } else {
        emit initStage1();
    }
}
