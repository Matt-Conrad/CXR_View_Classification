#include "storeupdater.h"

StoreUpdater::StoreUpdater(std::string columnsInfo, std::string configFilename, std::string sectionName, std::string folderFullPath, std::string filename) : QObject()
{
    StoreUpdater::columnsInfo = columnsInfo;
    StoreUpdater::configFilename = configFilename;
    StoreUpdater::sectionName = sectionName;
    StoreUpdater::folderFullPath = folderFullPath;

    StoreUpdater::dbInfo = config::getSection(configFilename, "postgresql");

    StoreUpdater::metadataTableName = config::getSection(configFilename, "table_info").get<std::string>("metadata_table_name");

    StoreUpdater::expected_num_files = expected_num_files_in_dataset.at(filename);
}

void StoreUpdater::updateProgressBar()
{
    emit attemptUpdateText("Storing metadata");
    emit attemptUpdateProBarBounds(0, expected_num_files);

    while (!bdo::tableExists(dbInfo, metadataTableName)) {
        ;
    }

    emit attemptUpdateProBarValue(0);
    while (bdo::countRecords(dbInfo, metadataTableName) < expected_num_files) {
        emit attemptUpdateProBarValue(bdo::countRecords(dbInfo, metadataTableName));
    }
    emit attemptUpdateProBarValue(bdo::countRecords(dbInfo, metadataTableName));
    emit attemptUpdateText("Done storing metadata");

    emit finished();
}



