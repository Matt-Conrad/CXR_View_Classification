#ifndef POSTGRES_H
#define POSTGRES_H

#include <pqxx/pqxx>
#include <string>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include "confighandler.h"

class DatabaseHandler
{
public:
    DatabaseHandler(ConfigHandler *);

    bool dbExists();
    void createNewDb();
    bool tableExists(std::string);
    void addTableToDb(std::string, std::string, std::string);
    int countRecords(std::string);
    pqxx::connection * openConnection();
    void deleteConnection(pqxx::connection * &);

private:
    ConfigHandler * configHandler;

    std::string host;
    std::string port;
    std::string database;
    std::string user;
    std::string password;
};

#endif // POSTGRES_H
