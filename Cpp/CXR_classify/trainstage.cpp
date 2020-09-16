#include "trainstage.h"

TrainStage::TrainStage(ConfigHandler * configHandler, DatabaseHandler * dbHandler) : Stage1()
{
    trainer = new Trainer(configHandler, dbHandler);
}

void TrainStage::train()
{
    threadpool->start(trainer);
}
