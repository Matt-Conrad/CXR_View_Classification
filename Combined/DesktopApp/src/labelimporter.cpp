#include "labelimporter.h"

LabelImporter::LabelImporter()
{

}

void LabelImporter::run()
{
    std::string elementsJson = configHandler->getColumnsInfoPath();
    std::string labelTableName = configHandler->getTableName("label");

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

    dbHandler->executeQuery(dbHandler->connection, sqlQuery);
}

LabelImporter * LabelImporter_new() { 
    return new LabelImporter(); 
}

void LabelImporter_run(LabelImporter * labelImporter) {
    labelImporter->run();
}
