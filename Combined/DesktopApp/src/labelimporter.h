#ifndef LABELIMPORTER_H
#define LABELIMPORTER_H

#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <pqxx/pqxx>
#include "confighandler.h"
#include "databasehandler.h"

class LabelImporter
{
public:
    LabelImporter();
    void run();

private:
    ConfigHandler * configHandler = new ConfigHandler("config.ini");
    DatabaseHandler * dbHandler = new DatabaseHandler(configHandler);
};

// These functions can be called from "C" 
extern "C" {
    LabelImporter * LabelImporter_new();
    void LabelImporter_run(LabelImporter *);
}

#endif // LABELIMPORTER_H
