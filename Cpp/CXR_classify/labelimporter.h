#ifndef LABELIMPORTER_H
#define LABELIMPORTER_H

#include <QObject>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <boost/algorithm/string/join.hpp>
#include <pqxx/pqxx>
#include <iostream>
#include "confighandlers.h"
#include "basicDbOps.h"

class LabelImporter : public QObject
{
    Q_OBJECT
public:
    LabelImporter(std::string, std::string, std::string, std::string, std::string);

private:
    std::string labelTableName;
    std::string csvFullPath;
    std::string elementsJson;
    std::string dbConfigFilename;
    std::string sectionName;

    boost::property_tree::ptree dbInfo;

public slots:
    void importLabels();

signals:
    void finished();
    void attemptUpdateText(QString);
};

#endif // LABELIMPORTER_H
