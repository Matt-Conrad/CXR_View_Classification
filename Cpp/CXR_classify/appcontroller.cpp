#include "appcontroller.h"


AppController::AppController()
{
    initGuiState();
}

void AppController::initGuiState()
{
    mainWindow.setWindowIcon(QIcon("../../miscellaneous/icon.jpg"));

    if (!std::filesystem::exists(filename) && !std::filesystem::exists(folder_full_path)) {
        connect(this, SIGNAL (initStage1()), &mainWindow, SLOT (stage1_ui()));
        emit initStage1();
    } else if (std::filesystem::exists(filename) && !std::filesystem::exists(folder_full_path)) {
        connect(this, SIGNAL (initStage2()), &mainWindow, SLOT (stage2_ui()));
        emit initStage2();
    } else if (std::filesystem::exists(filename) && std::filesystem::exists(folder_full_path)) {
        connect(this, SIGNAL (initStage3()), &mainWindow, SLOT (stage3_ui()));
        emit initStage3();
    }
}
