#ifndef STORESTAGE_H
#define STORESTAGE_H

#include <QObject>
#include "confighandler.h"
#include "stage1.h"
#include "storer.h"

class StoreStage : public Stage1
{
    Q_OBJECT
public:
    StoreStage(ConfigHandler *, DatabaseHandler *);
    Storer * storer;

public slots:
    void store();
};

#endif // STORESTAGE_H
