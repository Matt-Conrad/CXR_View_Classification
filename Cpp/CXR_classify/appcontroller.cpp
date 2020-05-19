#include "appcontroller.h"


AppController::AppController()
{
    initGuiState();
}

void AppController::initGuiState()
{
    mainWindow.setWindowIcon(QIcon("../../miscellaneous/icon.jpg"));

    if (!std::filesystem::exists(downloader->filename) && !std::filesystem::exists(downloader->folder_full_path)) {
        mainWindow.stage1_ui();
    } else if (std::filesystem::exists(downloader->filename) && !std::filesystem::exists(downloader->folder_full_path)) {
        mainWindow.stage2_ui();
    } else if (std::filesystem::exists(downloader->filename) && std::filesystem::exists(downloader->folder_full_path)) {
        mainWindow.stage3_ui();
    }
}
