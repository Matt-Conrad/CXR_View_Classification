#ifndef FEATCALCUPDATER_H
#define FEATCALCUPDATER_H

#include <QObject>
#include <pqxx/pqxx>
#include <iostream>
#include <boost/property_tree/ptree.hpp>
#include "unpackupdater.h"
#include "confighandlers.h"
#include "basicDbOps.h"

class FeatCalcUpdater : public QObject
{
    Q_OBJECT
friend class AppController;

public:
    FeatCalcUpdater(std::string, std::string, std::string, std::string, std::string);

private:
    std::string columnsInfo;
    std::string configFilename;
    std::string sectionName;
    std::string folderFullPath;

    boost::property_tree::ptree dbInfo;

    std::string featTableName;

    quint64 expected_num_files;

public slots:
    void updateProgressBar();

signals:
    void finished();
    void attemptUpdateProBarValue(quint64);
    void attemptUpdateProBarBounds(quint64, quint64);
    void attemptUpdateText(QString);

};

#endif // FEATCALCUPDATER_H
