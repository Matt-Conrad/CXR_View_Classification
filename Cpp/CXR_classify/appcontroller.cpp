#include "appcontroller.h"


AppController::AppController()
{
    initGuiState();
}

void AppController::initGuiState()
{
    mainWindow.setWindowIcon(QIcon("../../miscellaneous/icon.jpg"));

    if (!std::filesystem::exists(filename) && !std::filesystem::exists(folder_full_path) && !tableExists(metaTableName)) {
        connect(this, SIGNAL (initStage1()), &mainWindow, SLOT (stage1_ui()));
        emit initStage1();
    } else if (std::filesystem::exists(filename) && !std::filesystem::exists(folder_full_path) && !tableExists(metaTableName)) {
        connect(this, SIGNAL (initStage2()), &mainWindow, SLOT (stage2_ui()));
        emit initStage2();
    } else if (std::filesystem::exists(filename) && std::filesystem::exists(folder_full_path) && !tableExists(metaTableName)) {
        connect(this, SIGNAL (initStage3()), &mainWindow, SLOT (stage3_ui()));
        emit initStage3();
    } else if (std::filesystem::exists(filename) && std::filesystem::exists(folder_full_path) && tableExists(metaTableName) && !tableExists(featTableName)) {
        connect(this, SIGNAL (initStage4()), &mainWindow, SLOT (stage4_ui()));
        emit initStage4();
    } else if (std::filesystem::exists(filename) && std::filesystem::exists(folder_full_path) && tableExists(metaTableName) && tableExists(featTableName) && !tableExists(labelTableName)) {
        connect(this, SIGNAL (initStage5()), &mainWindow, SLOT (stage5_ui()));
        emit initStage5();
    }
}

bool AppController::tableExists(std::string tableName)
{
    try
    {
        // Connect to the database
        pqxx::connection c("host=" + host + " port=" + port + " dbname=" + database + " user=" + user + " password=" + password);

        // Start a transaction
        pqxx::work w(c);

        // Execute query
        pqxx::result r = w.exec("SELECT * FROM information_schema.tables WHERE table_name=\'" + tableName + "\';");

        std::cout << "" << std::endl;

        // Return based on result
        if (r.size() == 0) {
            return false;
        } else {
            return true;
        }
    }
    catch (std::exception const &e)
    {
        return false;
    }
}
