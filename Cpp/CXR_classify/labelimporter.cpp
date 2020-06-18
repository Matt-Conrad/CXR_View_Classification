#include "labelimporter.h"

LabelImporter::LabelImporter(std::string tableName, std::string csvFullPath, std::string elementsJson, std::string dbConfigFilename, std::string sectionName) : QObject()
{
    LabelImporter::tableName = tableName;
    LabelImporter::csvFullPath = csvFullPath;
    LabelImporter::elementsJson = elementsJson;
    LabelImporter::dbConfigFilename = dbConfigFilename;
    LabelImporter::sectionName = sectionName;

    LabelImporter::host = configParser(dbConfigFilename, "postgresql").get<std::string>("host");
    LabelImporter::port = configParser(dbConfigFilename, "postgresql").get<std::string>("port");
    LabelImporter::database = configParser(dbConfigFilename, "postgresql").get<std::string>("database");
    LabelImporter::user = configParser(dbConfigFilename, "postgresql").get<std::string>("user");
    LabelImporter::password = configParser(dbConfigFilename, "postgresql").get<std::string>("password");
}

void LabelImporter::importLabels()
{
    emit attemptUpdateText("Attempting to import image labels");
    addTableToDb();

    // Open the json with the list of elements we're interested in
    boost::property_tree::ptree columnsJson;
    boost::property_tree::read_json(elementsJson, columnsJson);
    boost::property_tree::ptree elements = columnsJson.get_child("labels");

    // Make the SQL query
    std::string sqlQuery = "COPY " + tableName + " (file_name, file_path, ";
    for (boost::property_tree::ptree::value_type & column : elements) {
        if (column.second.get<std::string>("calculation_only") == "false") {
            sqlQuery += (column.first + ",");
        }
    }
    sqlQuery = sqlQuery.substr(0, sqlQuery.length() - 1) + ") FROM '" + csvFullPath + "' DELIMITER ',' CSV HEADER;";

    try
    {
        // Connect to the database
        pqxx::connection c("host=" + host + " port=" + port + " dbname=" + database + " user=" + user + " password=" + password);

        // Start a transaction
        pqxx::work w(c);

        // Execute query
        pqxx::result r = w.exec(sqlQuery);

        // Commit your transaction
        w.commit();
    }
    catch (std::exception const &e)
    {
        std::cout << e.what() << std::endl;
    }
    emit attemptUpdateText("Finished importing image labels");
    emit finished();
}

void LabelImporter::addTableToDb()
{
    boost::property_tree::ptree columnsJson;
    boost::property_tree::read_json(elementsJson, columnsJson);
    boost::property_tree::ptree elements = columnsJson.get_child("labels");

    std::string sqlQuery = "CREATE TABLE " + tableName + " (file_name VARCHAR(255) PRIMARY KEY, file_path VARCHAR(255)";

    for (boost::property_tree::ptree::value_type & column : elements) {
        sqlQuery += (", " + column.first + " " + column.second.get<std::string>("db_datatype"));
    }
    sqlQuery += ");";

    try
    {
        // Connect to the database
        pqxx::connection c("host=" + host + " port=" + port + " dbname=" + database + " user=" + user + " password=" + password);

        // Start a transaction
        pqxx::nontransaction w(c);

        // Execute query
        pqxx::result r = w.exec(sqlQuery);

        // Commit your transaction
        w.commit();
    }
    catch (std::exception const &e)
    {
        std::cerr << e.what() << std::endl;
    }
}