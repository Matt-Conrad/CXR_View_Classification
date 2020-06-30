#ifndef POSTGRES_H
#define POSTGRES_H

#include <iostream>
#include <pqxx/pqxx>
#include <string>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <boost/algorithm/string/join.hpp>

namespace bdo {
    bool dbExists(std::string, std::string, std::string, std::string, std::string);
    void createNewDb(std::string, std::string, std::string);
    bool tableExists(std::string, std::string, std::string, std::string, std::string, std::string);
    void addTableToDb(std::string, std::string, std::string, std::string, std::string, std::string, std::string, std::string);
}

#endif // POSTGRES_H
