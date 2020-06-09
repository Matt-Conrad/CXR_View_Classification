#include "featcalcupdater.h"

FeatCalcUpdater::FeatCalcUpdater(std::string columnsInfo, std::string configFilename, std::string sectionName, std::string folderFullPath) : QObject()
{
    FeatCalcUpdater::columnsInfo = columnsInfo;
    FeatCalcUpdater::configFilename = configFilename;
    FeatCalcUpdater::sectionName = sectionName;
    FeatCalcUpdater::folderFullPath = folderFullPath;

    FeatCalcUpdater::host = configParser(configFilename, "postgresql").get<std::string>("host");
    FeatCalcUpdater::port = configParser(configFilename, "postgresql").get<std::string>("port");
    FeatCalcUpdater::database = configParser(configFilename, "postgresql").get<std::string>("database");
    FeatCalcUpdater::user = configParser(configFilename, "postgresql").get<std::string>("user");
    FeatCalcUpdater::password = configParser(configFilename, "postgresql").get<std::string>("password");

    FeatCalcUpdater::featTableName = configParser(configFilename, "table_info").get<std::string>("features_table_name");
}

void FeatCalcUpdater::updateProgressBar()
{
    emit attemptUpdateText("Calculating features");
    emit attemptUpdateProBarBounds(0, expected_num_files);

    while (!tableExists(featTableName)) {
        ;
    }

    emit attemptUpdateProBarValue(0);
    while (countRecords() < expected_num_files) {
        emit attemptUpdateProBarValue(countRecords());
    }
    emit attemptUpdateProBarValue(countRecords());
    emit attemptUpdateText("Done calculating features");

    emit finished();
}

quint64 FeatCalcUpdater::countRecords() {
    try
    {
        // Connect to the database
        pqxx::connection c("host=" + host + " port=" + port + " dbname=" + database + " user=" + user + " password=" + password);

        // Start a transaction
        pqxx::work w(c);

        // Execute query
        pqxx::result r = w.exec("SELECT COUNT(*) FROM " + featTableName + ";");

        w.commit();

        // Return based on result
        return r[0][0].as<int>();
    }
    catch (std::exception const &e)
    {
        std::cerr << e.what() << std::endl;
    }
}

bool FeatCalcUpdater::tableExists(std::string tableName)
{
    try
    {
        // Connect to the database
        pqxx::connection c("host=" + host + " port=" + port + " dbname=" + database + " user=" + user + " password=" + password);

        // Start a transaction
        pqxx::work w(c);

        // Execute query
        pqxx::result r = w.exec("SELECT * FROM information_schema.tables WHERE table_name=\'" + tableName + "\';");

        w.commit();

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
