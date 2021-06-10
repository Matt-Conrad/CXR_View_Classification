#include "labelimporter.h"

#include <iostream>

LabelImporter::LabelImporter(ConfigHandler * configHandler, DatabaseHandler * dbHandler) : Runnable(configHandler, dbHandler)
{

}

void LabelImporter::run()
{
    // std::chrono::steady_clock::time_point begin = std::chrono::steady_clock::now();
    logger->info("Importing label data from CSV");

    std::string elementsJson = configHandler->getColumnsInfoName();
    std::string labelTableName = configHandler->getTableName("label");

    emit attemptUpdateText("Attempting to import image labels");
    dbHandler->addTableToDb(elementsJson, "labels", labelTableName);

    // Open the json with the list of elements we're interested in
    boost::property_tree::ptree columnsJson;
    boost::property_tree::read_json(elementsJson, columnsJson);
    boost::property_tree::ptree elements = columnsJson.get_child("labels");

    // Make the SQL query
    std::string sqlQuery = "COPY " + labelTableName + " (file_name, file_path, ";
    for (boost::property_tree::ptree::value_type & column : elements) {
        if (column.second.get<std::string>("calculation_only") == "false") {
            sqlQuery += (column.first + ",");
        }
    }
    sqlQuery = sqlQuery.substr(0, sqlQuery.length() - 1) + ") FROM '" + configHandler->getCsvPath() + "' DELIMITER ',' CSV HEADER;";

    dbHandler->executeQuery(dbHandler->connection, sqlQuery);

    logger->info("Done importing label data");

    // std::chrono::steady_clock::time_point end = std::chrono::steady_clock::now();
    // std::cout << "Time difference = " << (std::chrono::duration_cast<std::chrono::nanoseconds> (end - begin).count())/1000000000.0 << "[s]" << std::endl;
    emit attemptUpdateText("Finished importing image labels");
    emit finished();
}
