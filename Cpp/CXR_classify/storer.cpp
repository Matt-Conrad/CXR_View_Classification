#include "storer.h"

Storer::Storer(std::string columnsInfo, std::string configFilename, std::string sectionName, std::string folderFullPath) : QObject()
{
    Storer::columnsInfo = columnsInfo;
    Storer::configFilename = configFilename;
    Storer::sectionName = sectionName;
    Storer::folderFullPath = folderFullPath;

    Storer::host = configParser(configFilename, "postgresql").get<std::string>("host");
    Storer::port = configParser(configFilename, "postgresql").get<std::string>("port");
    Storer::database = configParser(configFilename, "postgresql").get<std::string>("database");
    Storer::user = configParser(configFilename, "postgresql").get<std::string>("user");
    Storer::password = configParser(configFilename, "postgresql").get<std::string>("password");

    Storer::metadataTableName = configParser(configFilename, "table_info").get<std::string>("metadata_table_name");

    Storer::dicomToDb();
}

void Storer::dicomToDb()
{
    // Create the database if it isn't already there
    if (!dbExists()){
        createNewDb();
    }

    // Create table if it isn't already there
    if (!tableExists(metadataTableName)) {
        addTableToDb();
    }

    // Open the json with the list of elements we're interested in
    boost::property_tree::ptree columnsJson;
    boost::property_tree::read_json(columnsInfo, columnsJson);
    boost::property_tree::ptree elements = columnsJson.get_child("elements");

    for (auto & p : std::filesystem::recursive_directory_iterator(folderFullPath)) {
        if (p.path().extension() == ".dcm") {


//            DicomImage * image = new DicomImage(p.path().string().c_str());
            std::cout << p.path().string() << std::endl;
//            try
//            {
//                // Connect to the database
//                pqxx::connection c("host=" + host + " port=" + port + " dbname=" + database + " user=" + user + " password=" + password);

//                // Start a transaction
//                pqxx::work w(c);

//                // Create SQL query
//                std::string sqlQuery = createSqlQuery(metadataTableName, elements, p.path().string());

//                // Execute query
//                pqxx::result r = w.exec("");
//            }
//            catch (std::exception const &e)
//            {
//              std::cerr << e.what() << std::endl;
//            }

        }
    }
}

std::string Storer::createSqlQuery(std::string, boost::property_tree::ptree, std::string)
{
    return "test";
}

void Storer::addTableToDb()
{
    boost::property_tree::ptree columnsJson;
    boost::property_tree::read_json(columnsInfo, columnsJson);
    boost::property_tree::ptree elements = columnsJson.get_child("elements");

    std::string sqlQuery = "CREATE TABLE " + metadataTableName + " (file_name VARCHAR(255) PRIMARY KEY, file_path VARCHAR(255)";

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

bool Storer::tableExists(std::string tableName)
{
    try
    {
        // Connect to the database
        pqxx::connection c("host=" + host + " port=" + port + " dbname=" + database + " user=" + user + " password=" + password);

        // Start a transaction
        pqxx::work w(c);

        // Execute query
        pqxx::result r = w.exec("SELECT * FROM information_schema.tables WHERE table_name=\'" + tableName + "\';");

        // Return based on result
        if (r.size() == 0) {
            return false;
        } else {
            return true;
        }
    }
    catch (std::exception const &e)
    {
      std::cerr << e.what() << std::endl;
    }
}

void Storer::createNewDb()
{
    try
    {
        // Connect to the database
        pqxx::connection c("host=" + host + " port=" + port + " dbname=postgres user=postgres password=postgres");

        // Start a transaction
        pqxx::nontransaction w(c);

        // Execute query
        pqxx::result r = w.exec("CREATE DATABASE " + database + ';');

        // Commit your transaction
        w.commit();
    }
    catch (std::exception const &e)
    {
      std::cerr << e.what() << std::endl;
    }
}

bool Storer::dbExists()
{
    try
    {
        // Connect to the database
        pqxx::connection c("host=" + host + " port=" + port + " dbname=postgres user=" + user + " password=" + password);

        // Start a transaction
        pqxx::work w(c);

        // Execute query
        pqxx::result r = w.exec("SELECT datname FROM pg_catalog.pg_database WHERE datname=\'" + database + "\'");

        // Return based on result
        if (r.size() == 0) {
            return false;
        } else {
            return true;
        }

    }
    catch (std::exception const &e)
    {
      std::cerr << e.what() << std::endl;
    }
}
