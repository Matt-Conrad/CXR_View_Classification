#ifndef POSTGRES_H
#define POSTGRES_H

#include <pqxx/pqxx>
#include <string>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include "confighandler.h"
#include "spdlog/spdlog.h"

class DatabaseHandler
{
public:
    DatabaseHandler(ConfigHandler *);
    ~DatabaseHandler();

    bool dbExists();
    void createNewDb();
    bool tableExists(std::string);
    void addTableToDb(std::string, std::string, std::string);
    int countRecords(std::string);
    pqxx::connection * openConnection(bool openDefault = false);
    void closeConnection(pqxx::connection * &);
    pqxx::work * openCursor(pqxx::connection &);
    pqxx::nontransaction * openNonTransCursor(pqxx::connection &);
    void closeCursor(pqxx::work *);
    void checkServerConnection();

    pqxx::result executeQuery(pqxx::connection * connection, std::string query);
    pqxx::result executeNonTransQuery(pqxx::connection * connection, std::string query);

    pqxx::connection * connection;
    pqxx::connection * defaultConnection;
private:
    ConfigHandler * configHandler;

    std::shared_ptr<spdlog::logger> logger;

    std::string host;
    std::string port;
    std::string database;
    std::string user;
    std::string password;
};

#endif // POSTGRES_H
