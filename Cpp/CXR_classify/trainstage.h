#ifndef TRAINSTAGE_H
#define TRAINSTAGE_H

#include <QObject>
#include "databasehandler.h"
#include "confighandler.h"
#include "stage1.h"
#include "trainer.h"

class TrainStage : public Stage1
{
    Q_OBJECT
public:
    TrainStage(ConfigHandler *, DatabaseHandler *);
    Trainer * trainer;

public slots:
    void train();
};

#endif // TRAINSTAGE_H
