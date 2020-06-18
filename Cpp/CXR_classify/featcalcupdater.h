#ifndef FEATCALCUPDATER_H
#define FEATCALCUPDATER_H

#include <QObject>
#include <pqxx/pqxx>
#include <iostream>
#include "unpackupdater.h"
#include "confighandlers.h"

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

    std::string host;
    std::string port;
    std::string database;
    std::string user;
    std::string password;

    std::string featTableName;

    quint64 expected_num_files;

    bool tableExists(std::string);
    quint64 countRecords();

public slots:
    void updateProgressBar();

signals:
    void finished();
    void attemptUpdateProBarValue(quint64);
    void attemptUpdateProBarBounds(quint64, quint64);
    void attemptUpdateText(QString);

};

#endif // FEATCALCUPDATER_H
