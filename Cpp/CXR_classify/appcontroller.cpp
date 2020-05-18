#include "appcontroller.h"
#include <filesystem>
AppController::AppController()
{
    initGuiState();
}

void AppController::initGuiState()
{
    mainWindow.setWindowIcon(QIcon("../../miscellaneous/icon.jpg"));

    if (!std::filesystem::exists(downloader.filename)) {
        mainWindow.stage1_ui();
    } else if (std::filesystem::exists(downloader.filename)) {
        mainWindow.stage2_ui();
    }
}
