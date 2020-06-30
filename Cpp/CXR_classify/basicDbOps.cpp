#include "basicDbOps.h"

bool bdo::dbExists(std::string host, std::string port, std::string user, std::string password, std::string database)
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

void bdo::createNewDb(std::string host, std::string port, std::string database)
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

bool bdo::tableExists(std::string host, std::string port, std::string user, std::string password, std::string database, std::string tableName)
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

void bdo::addTableToDb(std::string host, std::string port, std::string user, std::string password, std::string database, std::string columnsInfo, std::string section, std::string tableName)
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
      std::cerr << e.what() << std::endl;
    }
}
