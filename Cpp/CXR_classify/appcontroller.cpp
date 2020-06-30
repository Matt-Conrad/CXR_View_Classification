#include "appcontroller.h"


AppController::AppController()
{
    initGuiState();
}

void AppController::initGuiState()
{
    mainWindow.setWindowIcon(QIcon("../../miscellaneous/icon.jpg"));

    if (!std::filesystem::exists(filename) && !std::filesystem::exists(folder_full_path) && !bdo::tableExists(host, port, user, password, database, metaTableName)) {
        connect(this, SIGNAL (initStage1()), &mainWindow, SLOT (stage1_ui()));
        emit initStage1();
    } else if (std::filesystem::exists(filename) && !std::filesystem::exists(folder_full_path) && !bdo::tableExists(host, port, user, password, database, metaTableName)) {
        connect(this, SIGNAL (initStage2()), &mainWindow, SLOT (stage2_ui()));
        emit initStage2();
    } else if (std::filesystem::exists(filename) && std::filesystem::exists(folder_full_path) && !bdo::tableExists(host, port, user, password, database, metaTableName)) {
        connect(this, SIGNAL (initStage3()), &mainWindow, SLOT (stage3_ui()));
        emit initStage3();
    } else if (std::filesystem::exists(filename) && std::filesystem::exists(folder_full_path) && bdo::tableExists(host, port, user, password, database, metaTableName) && !bdo::tableExists(host, port, user, password, database, featTableName)) {
        connect(this, SIGNAL (initStage4()), &mainWindow, SLOT (stage4_ui()));
        emit initStage4();
    } else if (std::filesystem::exists(filename) && std::filesystem::exists(folder_full_path) && bdo::tableExists(host, port, user, password, database, metaTableName) && bdo::tableExists(host, port, user, password, database, featTableName) && !bdo::tableExists(host, port, user, password, database, labelTableName)) {
        connect(this, SIGNAL (initStage5()), &mainWindow, SLOT (stage5_ui()));
        emit initStage5();
    } else if (std::filesystem::exists(filename) && std::filesystem::exists(folder_full_path) && bdo::tableExists(host, port, user, password, database, metaTableName) && bdo::tableExists(host, port, user, password, database, featTableName) && bdo::tableExists(host, port, user, password, database, labelTableName)) {
        connect(this, SIGNAL (initStage6()), &mainWindow, SLOT (stage6_ui()));
        emit initStage6();
    }
}
