#include "labelimporter.h"

LabelImporter::LabelImporter(std::string csvFullPath, std::string elementsJson, ConfigHandler * configHandler) : QObject()
{
    LabelImporter::csvFullPath = csvFullPath;
    LabelImporter::elementsJson = elementsJson;
    LabelImporter::configHandler = configHandler;
}

void LabelImporter::importLabels()
{
    boost::property_tree::ptree dbInfo = configHandler->getSection("postgresql");
    std::string labelTableName = configHandler->getSetting("table_info", "label_table_name");

    emit attemptUpdateText("Attempting to import image labels");
    bdo::addTableToDb(dbInfo, elementsJson, "labels", labelTableName);

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
    sqlQuery = sqlQuery.substr(0, sqlQuery.length() - 1) + ") FROM '" + csvFullPath + "' DELIMITER ',' CSV HEADER;";

    try
    {
        // Connect to the database
        pqxx::connection * connection = bdo::openConnection(dbInfo);

        // Start a transaction
        pqxx::work w(*connection);

        // Execute query
        pqxx::result r = w.exec(sqlQuery);

        // Commit your transaction
        w.commit();

        bdo::deleteConnection(connection);
    }
    catch (std::exception const &e)
    {
        std::cout << e.what() << std::endl;
    }
    emit attemptUpdateText("Finished importing image labels");
    emit finished();
}
