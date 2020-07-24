#ifndef STORER_H
#define STORER_H

#include <QObject>
#include <string>
#include <pqxx/pqxx>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <boost/algorithm/string/join.hpp>
#include <filesystem>
#include <vector>
#include <dcmtk/dcmdata/dcfilefo.h>
#include <dcmtk/dcmdata/dctagkey.h>
#include "confighandlers.h"
#include "basicDbOps.h"
#include "stage.h"

class Storer : public Stage
{
    Q_OBJECT

public:
    Storer(ConfigHandler *, DatabaseHandler *);

public slots:
    void dicomToDb();

private:
    DatabaseHandler * dbHandler;

    std::string createSqlQuery(std::string, boost::property_tree::ptree, std::string);
};

#endif // STORER_H
