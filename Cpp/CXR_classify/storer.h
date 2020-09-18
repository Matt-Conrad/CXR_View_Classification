#ifndef STORER_H
#define STORER_H

#include <string>
#include <pqxx/pqxx>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <boost/algorithm/string/join.hpp>
#include <filesystem>
#include <vector>
#include <dcmtk/dcmdata/dcfilefo.h>
#include <dcmtk/dcmdata/dctagkey.h>
#include "confighandler.h"
#include "databasehandler.h"
#include "runnable.h"

class Storer : public Runnable
{
public:
    Storer(ConfigHandler *, DatabaseHandler *);

private:
    std::string createSqlQuery(std::string, boost::property_tree::ptree, std::string);

public slots:
    void run();
};

#endif // STORER_H
