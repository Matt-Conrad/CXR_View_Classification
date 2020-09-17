#ifndef STORESTAGE_H
#define STORESTAGE_H

#include <QObject>
#include "databasehandler.h"
#include "confighandler.h"
#include "stage.h"
#include "storer.h"

class StoreStage : public Stage
{
    Q_OBJECT
public:
    StoreStage(ConfigHandler *, DatabaseHandler *);
    Storer * storer;

public slots:
    void store();
};

#endif // STORESTAGE_H
