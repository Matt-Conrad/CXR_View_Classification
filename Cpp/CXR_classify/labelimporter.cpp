#include "labelimporter.h"

LabelImporter::LabelImporter(ConfigHandler * configHandler, DatabaseHandler * dbHandler) : Runnable(configHandler, dbHandler)
{

}

void LabelImporter::run()
{
    std::string elementsJson = configHandler->getColumnsInfoPath();
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
    sqlQuery = sqlQuery.substr(0, sqlQuery.length() - 1) + ") FROM '" + configHandler->getParentFolder() + "/" + configHandler->getCsvPath() + "' DELIMITER ',' CSV HEADER;";

    try
    {
        // Connect to the database
        pqxx::connection * connection = dbHandler->openConnection();

        // Start a transaction
        pqxx::work w(*connection);

        // Execute query
        pqxx::result r = w.exec(sqlQuery);

        // Commit your transaction
        w.commit();

        dbHandler->deleteConnection(connection);
    }
    catch (std::exception const &e)
    {
        // log e.what()
    }
    emit attemptUpdateText("Finished importing image labels");
    emit finished();
}
