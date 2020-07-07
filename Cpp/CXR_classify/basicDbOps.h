#ifndef POSTGRES_H
#define POSTGRES_H

#include <iostream>
#include <pqxx/pqxx>
#include <string>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <boost/algorithm/string/join.hpp>
#include "confighandlers.h"

namespace bdo {
    bool dbExists(boost::property_tree::ptree);
    void createNewDb(boost::property_tree::ptree);
    bool tableExists(boost::property_tree::ptree, std::string);
    void addTableToDb(boost::property_tree::ptree, std::string, std::string, std::string);
    int countRecords(boost::property_tree::ptree, std::string);
    pqxx::connection * openConnection(boost::property_tree::ptree);
    void deleteConnection(pqxx::connection * &);
}

#endif // POSTGRES_H
