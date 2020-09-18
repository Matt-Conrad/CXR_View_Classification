#ifndef LABELIMPORTER_H
#define LABELIMPORTER_H

#include <QObject>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <pqxx/pqxx>
#include "confighandler.h"
#include "databasehandler.h"
#include "runnable.h"

class LabelImporter : public Runnable
{
    Q_OBJECT
public:
    LabelImporter(ConfigHandler *, DatabaseHandler *);

public slots:
    void run();
};

#endif // LABELIMPORTER_H
