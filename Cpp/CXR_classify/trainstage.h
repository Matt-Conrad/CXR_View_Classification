#ifndef TRAINSTAGE_H
#define TRAINSTAGE_H

#include <QObject>
#include "databasehandler.h"
#include "confighandler.h"
#include "stage.h"
#include "trainer.h"

class TrainStage : public Stage
{
    Q_OBJECT
public:
    TrainStage(ConfigHandler *, DatabaseHandler *);
    Trainer * trainer;

public slots:
    void train();
};

#endif // TRAINSTAGE_H
