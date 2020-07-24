#ifndef LABELIMPORTER_H
#define LABELIMPORTER_H

#include <QObject>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <pqxx/pqxx>
#include "confighandlers.h"
#include "basicDbOps.h"
#include "stage.h"

class LabelImporter : public Stage
{
    Q_OBJECT
public:
    LabelImporter(ConfigHandler *, DatabaseHandler *);

private:
    DatabaseHandler * dbHandler;

public slots:
    void importLabels();

};

#endif // LABELIMPORTER_H
