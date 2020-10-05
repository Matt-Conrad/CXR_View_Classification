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

class Storer {
    public:
        Storer();
        void run();

    private:
        ConfigHandler * configHandler = new ConfigHandler("../../miscellaneous/config.ini");
        DatabaseHandler * dbHandler = new DatabaseHandler(configHandler);

        std::string createSqlQuery(std::string, boost::property_tree::ptree, std::string);
};

// These functions can be called from "C" 
#if __cplusplus
  extern "C" {
#endif

    Storer * Storer_new();
    void Storer_run(Storer *);

#if __cplusplus
}
#endif


#endif // STORER_H
