#ifndef LABELSTAGE_H
#define LABELSTAGE_H

#include <QObject>
#include "databasehandler.h"
#include "confighandler.h"
#include "stage1.h"
#include "labeler.h"
#include "runnable.h"

class LabelStage : public Stage1
{
    Q_OBJECT
public:
    LabelStage(ConfigHandler *, DatabaseHandler *);
    Labeler * labeler;

public slots:
    void label();
};

#endif // LABELSTAGE_H
