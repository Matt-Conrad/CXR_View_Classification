#include "databasehandler.h"

DatabaseHandler::DatabaseHandler(ConfigHandler * configHandler)
{
    configHandler = configHandler;
    boost::property_tree::ptree dbInfo = configHandler->getDbInfo();

    host = dbInfo.get<std::string>("host");
    port = dbInfo.get<std::string>("port");
    database = dbInfo.get<std::string>("database");
    user = dbInfo.get<std::string>("user");
    password = dbInfo.get<std::string>("password");

    defaultConnection = openConnection(true);

    // Create the database if it isn't already there
    if (!dbExists()){
        createNewDb();
    }

    inputConnection = openConnection();
    outputConnection = openConnection();

    connection = openConnection();
}

DatabaseHandler::~DatabaseHandler()
{
    closeConnection(inputConnection);
    closeConnection(outputConnection);
}

pqxx::connection * DatabaseHandler::openConnection(bool openDefault)
{
    pqxx::connection * connection;
    if (openDefault) {
        connection = new pqxx::connection("host=" + host + " port=" + port + " dbname=postgres" " user=" + user + " password=" + password);
    } else {
        connection = new pqxx::connection("host=" + host + " port=" + port + " dbname=" + database + " user=" + user + " password=" + password);
    }
    return connection;
}

void DatabaseHandler::closeConnection(pqxx::connection * & connection)
{
    delete connection;
}

pqxx::work * DatabaseHandler::openCursor(pqxx::connection & connection)
{
    return (new pqxx::work(connection));
}

pqxx::nontransaction * DatabaseHandler::openNonTransCursor(pqxx::connection & connection)
{
    return (new pqxx::nontransaction(connection));
}

void DatabaseHandler::closeCursor(pqxx::work * cursor)
{
    delete cursor;
}

void DatabaseHandler::checkServerConnection()
{
    ;
}

void DatabaseHandler::createNewDb()
{
    executeNonTransQuery(defaultConnection, "CREATE DATABASE " + database + ';');
}

bool DatabaseHandler::dbExists()
{
    std::string sqlQuery = "SELECT datname FROM pg_catalog.pg_database WHERE datname=\'" + database + "\'";

    pqxx::result result = executeQuery(defaultConnection, sqlQuery);

    if (result.size() == 0) {
        return false;
    } else {
        return true;
    }
}

bool DatabaseHandler::tableExists(std::string tableName)
{
    std::string sqlQuery = "SELECT * FROM information_schema.tables WHERE table_name=\'" + tableName + "\';";

    pqxx::result queryResult = executeQuery(connection, sqlQuery);

    if (queryResult.size() == 0) {
        return false;
    } else {
        return true;
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

    executeNonTransQuery(connection, sqlQuery);
}

int DatabaseHandler::countRecords(std::string tableName) {
    pqxx::result result = executeQuery(connection, "SELECT COUNT(*) FROM " + tableName + ";");
    return result[0][0].as<int>();
}

pqxx::connection * DatabaseHandler::getInputConnection() {
    return inputConnection;
}

pqxx::connection * DatabaseHandler::getOutputConnection() {
    return outputConnection;
}

pqxx::result DatabaseHandler::executeQuery(pqxx::connection * connection, std::string query)
{
    pqxx::work * cursor = openCursor(*connection);
    pqxx::result result;
    try {
        result = cursor->exec(query);
    } catch (std::exception const &e) {

    }
    cursor->commit();
    return result;
}

pqxx::result DatabaseHandler::executeNonTransQuery(pqxx::connection * connection, std::string query)
{
    pqxx::nontransaction * cursor = openNonTransCursor(*connection);
    pqxx::result result;
    try {
        result = cursor->exec(query);
    } catch (std::exception const &e) {

    }
    cursor->commit();
    return result;
}
