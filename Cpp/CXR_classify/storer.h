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
#include "unpacker.h"

class Storer : public QObject
{
    Q_OBJECT
public:
    Storer(ConfigHandler *);

public slots:
    void dicomToDb();

private:
    std::string columnsInfo;
    std::string folderFullPath;

    quint64 expected_num_files;

    ConfigHandler * configHandler;

    std::string createSqlQuery(std::string, boost::property_tree::ptree, std::string);

signals:
    void finished();
    void attemptUpdateProBarValue(quint64);
    void attemptUpdateProBarBounds(quint64, quint64);
    void attemptUpdateText(QString);
};

#endif // STORER_H
