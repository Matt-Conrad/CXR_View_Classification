#include "storer.h"

#include <chrono>
#include <iostream>

Storer::Storer(ConfigHandler * configHandler, DatabaseHandler * dbHandler) : Runnable(configHandler, dbHandler)
{

}

void Storer::run()
{
    std::chrono::steady_clock::time_point begin = std::chrono::steady_clock::now();
    emit attemptUpdateText("Storing metadata");
    emit attemptUpdateProBarBounds(0, expected_num_files);

    std::string metadataTableName = configHandler->getTableName("metadata");
    std::string columnsInfoName = configHandler->getColumnsInfoName();

    // Create table if it isn't already there
    if (!dbHandler->tableExists(metadataTableName)) {
        dbHandler->addTableToDb(columnsInfoName, "elements", metadataTableName);
    }

    logger->info("Attempting to store DICOM metadata from DCMs in a folder to Postgres DB");

    emit attemptUpdateProBarValue(0);

    // Open the json with the list of elements we're interested in
    boost::property_tree::ptree columnsJson;
    boost::property_tree::read_json(columnsInfoName, columnsJson);
    boost::property_tree::ptree elements = columnsJson.get_child("elements");

    quint64 storeCount = 0;
    for (auto & p : std::filesystem::recursive_directory_iterator(configHandler->getUnpackFolderPath())) {
        if (p.path().extension() == ".dcm") {
            logger->debug("Storing: {}", p.path().string());
            pqxx::result result = dbHandler->executeQuery(dbHandler->connection, createSqlQuery(metadataTableName, elements, p.path().string()));
            storeCount++;
            emit attemptUpdateProBarValue(storeCount);
        }
    }

    logger->info("Done storing metadata");

    std::chrono::steady_clock::time_point end = std::chrono::steady_clock::now();
    std::cout << "Time difference = " << (std::chrono::duration_cast<std::chrono::nanoseconds> (end - begin).count())/1000000000.0 << "[s]" << std::endl;
    emit attemptUpdateText("Done storing metadata");
    emit finished();
}

std::string Storer::createSqlQuery(std::string tableName, boost::property_tree::ptree elements, std::string filePath)
{
    // Read file
    DcmFileFormat file_format;
    OFCondition status = file_format.loadFile(filePath.c_str());

    // Go through the list of elements and try to read the value
    for (boost::property_tree::ptree::value_type & element : elements) {
        // Get tag and separate into its parts
        std::string tag = element.second.get<std::string>("tag");
        std::string groupNameString;
        std::string elementNumString;

        tag.erase(std::remove_if(tag.begin(), tag.end(), ::isspace), tag.end()); // Remove blank spaces
        std::istringstream tagStream(tag);
        getline(tagStream, groupNameString, ',');
        getline(tagStream, elementNumString, ',');

        uint16_t groupNameInt = std::stoul(groupNameString, nullptr, 16);
        uint16_t elementNumInt = std::stoul(elementNumString, nullptr, 16);

        DcmTagKey tagKey(groupNameInt, elementNumInt);
        OFString tagValue;
        file_format.getDataset()->findAndGetOFString(tagKey, tagValue);

        if (tagValue != "") {
            if (element.second.get<std::string>("db_datatype").find("INT") != std::string::npos) {
                element.second.put("value", tagValue.c_str());
            } else if (element.second.get<std::string>("db_datatype").find("CHAR") != std::string::npos) {
                std::string str(tagValue.c_str());
                element.second.put("value", "'" + str + "'");
            }
        } else {
            element.second.put("value", "NULL");
        }
    }

    std::vector<std::string> names{"file_name", "file_path"};
    std::vector<std::string> values{"'" + filePath.substr(filePath.find_last_of("/") + 1) + "'", "'" + filePath + "'"};

    for (boost::property_tree::ptree::value_type & element : elements) {
        if (!element.second.get<bool>("calculation_only")) {
            names.push_back(element.first);
            values.push_back(element.second.get<std::string>("value"));
        }
    }

    std::string sqlQuery = "INSERT INTO " + tableName + " (" + boost::algorithm::join(names, ", ") + ") VALUES (" + boost::algorithm::join(values, ", ") + ");";

    return sqlQuery;
}
