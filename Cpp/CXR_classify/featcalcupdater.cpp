#include "featcalcupdater.h"

FeatCalcUpdater::FeatCalcUpdater(std::string columnsInfo, std::string configFilename, std::string sectionName, std::string folderFullPath, std::string filename) : QObject()
{
    FeatCalcUpdater::columnsInfo = columnsInfo;
    FeatCalcUpdater::configFilename = configFilename;
    FeatCalcUpdater::sectionName = sectionName;
    FeatCalcUpdater::folderFullPath = folderFullPath;

    FeatCalcUpdater::dbInfo = config::getSection(configFilename, "postgresql");

    FeatCalcUpdater::featTableName = config::getSection(configFilename, "table_info").get<std::string>("features_table_name");
    FeatCalcUpdater::expected_num_files = expected_num_files_in_dataset.at(filename);
}

void FeatCalcUpdater::updateProgressBar()
{
    emit attemptUpdateText("Calculating features");
    emit attemptUpdateProBarBounds(0, expected_num_files);

    while (!bdo::tableExists(dbInfo, featTableName)) {
        ;
    }

    emit attemptUpdateProBarValue(0);
    while (bdo::countRecords(dbInfo, featTableName) < expected_num_files) {
        emit attemptUpdateProBarValue(bdo::countRecords(dbInfo, featTableName));
    }
    emit attemptUpdateProBarValue(bdo::countRecords(dbInfo, featTableName));
    emit attemptUpdateText("Done calculating features");

    emit finished();
}

