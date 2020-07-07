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
#include "basicDbOps.h"
#include "unpackupdater.h"

class Storer : public QObject
{
    Q_OBJECT
public:
    Storer(std::string, std::string, std::string, std::string, std::string);

public slots:
    void dicomToDb();

private:
    std::string columnsInfo;
    std::string configFilename;
    std::string sectionName;
    std::string folderFullPath;

    boost::property_tree::ptree dbInfo;

    std::string metadataTableName;
    quint64 expected_num_files;

    std::string createSqlQuery(std::string, boost::property_tree::ptree, std::string);

signals:
    void finished();
    void attemptUpdateProBarValue(quint64);
    void attemptUpdateProBarBounds(quint64, quint64);
    void attemptUpdateText(QString);
};

#endif // STORER_H
