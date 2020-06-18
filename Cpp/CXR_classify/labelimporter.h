#ifndef LABELIMPORTER_H
#define LABELIMPORTER_H

#include <QObject>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <boost/algorithm/string/join.hpp>
#include <pqxx/pqxx>
#include <iostream>
#include "confighandlers.h"

class LabelImporter : public QObject
{
    Q_OBJECT
public:
    LabelImporter(std::string, std::string, std::string, std::string, std::string);

private:
    std::string tableName;
    std::string csvFullPath;
    std::string elementsJson;
    std::string dbConfigFilename;
    std::string sectionName;

    std::string host;
    std::string port;
    std::string database;
    std::string user;
    std::string password;

    void addTableToDb();

public slots:
    void importLabels();

signals:
    void finished();
    void attemptUpdateText(QString);
};

#endif // LABELIMPORTER_H
