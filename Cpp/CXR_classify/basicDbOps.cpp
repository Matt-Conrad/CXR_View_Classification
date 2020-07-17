#include "basicDbOps.h"

DatabaseHandler::DatabaseHandler(ConfigHandler * configHandler)
{
    DatabaseHandler::configHandler = configHandler;
    boost::property_tree::ptree dbInfo = configHandler->getDbInfo();

    DatabaseHandler::host = dbInfo.get<std::string>("host");
    DatabaseHandler::port = dbInfo.get<std::string>("port");
    DatabaseHandler::database = dbInfo.get<std::string>("database");
    DatabaseHandler::user = dbInfo.get<std::string>("user");
    DatabaseHandler::password = dbInfo.get<std::string>("password");
}

bool DatabaseHandler::dbExists()
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
        // log e.what()
    }
}

void DatabaseHandler::createNewDb()
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
        // log e.what()
    }
}

bool DatabaseHandler::tableExists(std::string tableName)
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
        return false;
    }
}

void DatabaseHandler::addTableToDb(std::string columnsInfo, std::string section, std::string tableName)
{
    boost::property_tree::ptree columnsJson;
    boost::property_tree::read_json(columnsInfo, columnsJson);
    boost::property_tree::ptree elements = columnsJson.get_child(section);

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
        // log e.what()
    }
}

int DatabaseHandler::countRecords(std::string tableName) {
    try
    {
        // Connect to the database
        pqxx::connection c("host=" + host + " port=" + port + " dbname=" + database + " user=" + user + " password=" + password);

        // Start a transaction
        pqxx::work w(c);

        // Execute query
        pqxx::result r = w.exec("SELECT COUNT(*) FROM " + tableName + ";");

        w.commit();

        // Return based on result
        return r[0][0].as<int>();
    }
    catch (std::exception const &e)
    {
        // log e.what()
    }
}

pqxx::connection * DatabaseHandler::openConnection() {
    pqxx::connection * connection = new pqxx::connection("host=" + host + " port=" + port + " dbname=" + database + " user=" + user + " password=" + password);

    return connection;
}

void DatabaseHandler::deleteConnection(pqxx::connection * & connection) {
    delete connection;
}


