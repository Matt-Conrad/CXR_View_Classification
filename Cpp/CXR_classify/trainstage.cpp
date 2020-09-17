#include "trainstage.h"

TrainStage::TrainStage(ConfigHandler * configHandler, DatabaseHandler * dbHandler) : Stage()
{
    trainer = new Trainer(configHandler, dbHandler);
}

void TrainStage::train()
{
    threadpool->start(trainer);
}
