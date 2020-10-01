#include "databasehandler.h"

DatabaseHandler::DatabaseHandler(ConfigHandler * configHandler)
{
    DatabaseHandler::configHandler = configHandler;
    logger = spdlog::get(loggerName);
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

    connection = openConnection();
}

DatabaseHandler::~DatabaseHandler()
{
    closeConnection(defaultConnection);
    closeConnection(connection);
}

pqxx::connection * DatabaseHandler::openConnection(bool openDefault)
{
    std::string params;
    if (openDefault) {
        params = "host=" + host + " port=" + port + " dbname=postgres" " user=" + user + " password=" + password;
    } else {
        params = "host=" + host + " port=" + port + " dbname=" + database + " user=" + user + " password=" + password;
    }
    logger->info("Opening connection to DB: {}", params);
    return new pqxx::connection(params.c_str());
}

void DatabaseHandler::closeConnection(pqxx::connection * & connection)
{
    logger->info("Closing connection");
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
    logger->debug("Closing cursor");
    delete cursor;
}

void DatabaseHandler::checkServerConnection()
{
    logger->info("Checking connection to Postgres server");
    if (executeQuery(connection, "SELECT version();").size() != 0) {
        logger->info("Server is connected");
    } else {
        logger->info("Server is not connected");
    }
}

void DatabaseHandler::createNewDb()
{
    logger->info("Attempting to create a new DB");
    executeNonTransQuery(defaultConnection, "CREATE DATABASE " + database + ';');
}

bool DatabaseHandler::dbExists()
{
    std::string sqlQuery = "SELECT datname FROM pg_catalog.pg_database WHERE datname=\'" + database + "\'";

    pqxx::result result = executeQuery(defaultConnection, sqlQuery);
    bool exists;
    if (result.size() == 0) {
        exists = false;
    } else {
        exists = true;
    }
    logger->info("DB named {} exists: {}", database, exists);
    return exists;
}

bool DatabaseHandler::tableExists(std::string tableName)
{
    std::string sqlQuery = "SELECT * FROM information_schema.tables WHERE table_name=\'" + tableName + "\';";

    pqxx::result queryResult = executeQuery(connection, sqlQuery);
    bool exists;
    if (queryResult.size() == 0) {
        exists = false;
    } else {
        exists = true;
    }
    logger->info("Table named {} exists: {}", tableName, exists);
    return exists;
}

void DatabaseHandler::addTableToDb(std::string columnsInfo, std::string section, std::string tableName)
{
    logger->info("Attempting to add table");

    boost::property_tree::ptree columnsJson;
    boost::property_tree::read_json(columnsInfo, columnsJson);
    boost::property_tree::ptree elements = columnsJson.get_child(section);

    std::string sqlQuery = "CREATE TABLE " + tableName + " (file_name VARCHAR(255) PRIMARY KEY, file_path VARCHAR(255)";

    for (boost::property_tree::ptree::value_type & column : elements) {
        sqlQuery += (", " + column.first + " " + column.second.get<std::string>("db_datatype"));
    }
    sqlQuery += ");";

    executeQuery(connection, sqlQuery);
}

int DatabaseHandler::countRecords(std::string tableName) {
    pqxx::result result = executeQuery(connection, "SELECT COUNT(*) FROM " + tableName + ";");
    return result[0][0].as<int>();
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
