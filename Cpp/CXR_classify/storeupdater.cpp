#include "storeupdater.h"

StoreUpdater::StoreUpdater(std::string columnsInfo, std::string configFilename, std::string sectionName, std::string folderFullPath) : QObject()
{
    StoreUpdater::columnsInfo = columnsInfo;
    StoreUpdater::configFilename = configFilename;
    StoreUpdater::sectionName = sectionName;
    StoreUpdater::folderFullPath = folderFullPath;

    StoreUpdater::host = configParser(configFilename, "postgresql").get<std::string>("host");
    StoreUpdater::port = configParser(configFilename, "postgresql").get<std::string>("port");
    StoreUpdater::database = configParser(configFilename, "postgresql").get<std::string>("database");
    StoreUpdater::user = configParser(configFilename, "postgresql").get<std::string>("user");
    StoreUpdater::password = configParser(configFilename, "postgresql").get<std::string>("password");

    StoreUpdater::metadataTableName = configParser(configFilename, "table_info").get<std::string>("metadata_table_name");
}

void StoreUpdater::updateProgressBar()
{
    emit attemptUpdateText("Storing metadata");
    emit attemptUpdateProBarBounds(0, expected_num_files);

    while (!tableExists(metadataTableName)) {
        ;
    }

    emit attemptUpdateProBarValue(0);
    while (countRecords() < expected_num_files) {
        emit attemptUpdateProBarValue(countRecords());
    }
    emit attemptUpdateProBarValue(countRecords());
    emit attemptUpdateText("Done storing metadata");

    emit finished();
}

quint64 StoreUpdater::countRecords() {
    try
    {
        // Connect to the database
        pqxx::connection c("host=" + host + " port=" + port + " dbname=" + database + " user=" + user + " password=" + password);

        // Start a transaction
        pqxx::work w(c);

        // Execute query
        pqxx::result r = w.exec("SELECT COUNT(*) FROM " + metadataTableName + ";");

        w.commit();

        // Return based on result
        return r[0][0].as<int>();
    }
    catch (std::exception const &e)
    {
        std::cerr << e.what() << std::endl;
    }
}

bool StoreUpdater::tableExists(std::string tableName)
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
