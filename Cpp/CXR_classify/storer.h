#ifndef STORER_H
#define STORER_H

#include <QObject>
#include <sstream>
#include <iostream>
#include <string>
#include <pqxx/pqxx>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <boost/algorithm/string/join.hpp>
#include <filesystem>
#include <vector>
#include <dcmtk/dcmdata/dcfilefo.h>
#include <dcmtk/dcmdata/dcdeftag.h>
#include <thread>
#include <chrono>
#include "confighandlers.h"

class Storer : public QObject
{
    Q_OBJECT
public:
    Storer(std::string, std::string, std::string, std::string);

public slots:
    void dicomToDb();

private:
    std::string columnsInfo;
    std::string configFilename;
    std::string sectionName;
    std::string folderFullPath;

    std::string host;
    std::string port;
    std::string database;
    std::string user;
    std::string password;

    std::string metadataTableName;

    bool dbExists();
    void createNewDb();
    bool tableExists(std::string);
    void addTableToDb();
    std::string createSqlQuery(std::string, boost::property_tree::ptree, std::string);

signals:
    void finished();
};

#endif // STORER_H