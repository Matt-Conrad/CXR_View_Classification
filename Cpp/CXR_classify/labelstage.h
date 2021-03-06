#ifndef LABELSTAGE_H
#define LABELSTAGE_H

#include <QObject>
#include "databasehandler.h"
#include "confighandler.h"
#include "stage.h"
#include "manuallabeler.h"
#include "labelimporter.h"
#include "runnable.h"

class LabelStage : public Stage
{
    Q_OBJECT
public:
    LabelStage(ConfigHandler *, DatabaseHandler *);
    Runnable * labeler;

public slots:
    void label();
};

#endif // LABELSTAGE_H
