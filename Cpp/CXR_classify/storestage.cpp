#include "storestage.h"

StoreStage::StoreStage(ConfigHandler * configHandler, DatabaseHandler * dbHandler) : Stage()
{
    storer = new Storer(configHandler, dbHandler);
}

void StoreStage::store()
{
    threadpool->start(storer);
}
