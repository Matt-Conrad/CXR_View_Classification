#include "appcontroller.h"


AppController::AppController()
{
    configHandler->setSetting("misc", "parent_folder", boost::dll::program_location().parent_path().string());
    std::string tgz_filename = url.substr(url.find_last_of("/") + 1);
    configHandler->setSetting("misc", "tgz_filename", tgz_filename);
    configHandler->setSetting("misc", "dataset_folder_name", tgz_filename.substr(0, tgz_filename.find_last_of(".")));
    configHandler->setSetting("misc", "columns_info_relative_path", "../CXR_classify/columns_info.json");
    configHandler->setSetting("misc", "csv_relative_path", "/../CXR_classify/image_labels.csv");

    initGuiState();
}

AppController::~AppController()
{
    configHandler->~ConfigHandler();
}

void AppController::initGuiState()
{
    boost::property_tree::ptree dbInfo = configHandler->getSection("postgresql");
    std::string metadataTableName = configHandler->getSetting("table_info", "metadata_table_name");
    std::string featTableName = configHandler->getSetting("table_info", "features_table_name");
    std::string labelTableName = configHandler->getSetting("table_info", "label_table_name");

    mainWindow.setWindowIcon(QIcon("../../miscellaneous/icon.jpg"));

    std::string filename = configHandler->getSetting("misc","tgz_filename");
    std::string folder_full_path = configHandler->getSetting("misc","parent_folder") + "/" + configHandler->getSetting("misc","dataset_folder_name");

    if (!std::filesystem::exists(filename) && !std::filesystem::exists(folder_full_path) && !bdo::tableExists(dbInfo, metadataTableName)) {
        connect(this, SIGNAL (initStage1()), &mainWindow, SLOT (stage1_ui()));
        emit initStage1();
    } else if (std::filesystem::exists(filename) && !std::filesystem::exists(folder_full_path) && !bdo::tableExists(dbInfo, metadataTableName)) {
        connect(this, SIGNAL (initStage2()), &mainWindow, SLOT (stage2_ui()));
        emit initStage2();
    } else if (std::filesystem::exists(filename) && std::filesystem::exists(folder_full_path) && !bdo::tableExists(dbInfo, metadataTableName)) {
        connect(this, SIGNAL (initStage3()), &mainWindow, SLOT (stage3_ui()));
        emit initStage3();
    } else if (std::filesystem::exists(filename) && std::filesystem::exists(folder_full_path) && bdo::tableExists(dbInfo, metadataTableName) && !bdo::tableExists(dbInfo, featTableName)) {
        connect(this, SIGNAL (initStage4()), &mainWindow, SLOT (stage4_ui()));
        emit initStage4();
    } else if (std::filesystem::exists(filename) && std::filesystem::exists(folder_full_path) && bdo::tableExists(dbInfo, metadataTableName) && bdo::tableExists(dbInfo, featTableName) && !bdo::tableExists(dbInfo, labelTableName)) {
        connect(this, SIGNAL (initStage5()), &mainWindow, SLOT (stage5_ui()));
        emit initStage5();
    } else if (std::filesystem::exists(filename) && std::filesystem::exists(folder_full_path) && bdo::tableExists(dbInfo, metadataTableName) && bdo::tableExists(dbInfo, featTableName) && bdo::tableExists(dbInfo, labelTableName)) {
        connect(this, SIGNAL (initStage6()), &mainWindow, SLOT (stage6_ui()));
        emit initStage6();
    }
}
