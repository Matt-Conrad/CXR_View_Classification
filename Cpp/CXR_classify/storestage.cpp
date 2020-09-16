#include "storestage.h"

StoreStage::StoreStage(ConfigHandler * configHandler, DatabaseHandler * dbHandler) : Stage1()
{
    storer = new Storer(configHandler, dbHandler);
}

void StoreStage::store()
{
    threadpool->start(storer);
}
