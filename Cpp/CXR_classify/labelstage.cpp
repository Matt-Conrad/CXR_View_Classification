#include "labelstage.h"

LabelStage::LabelStage(ConfigHandler * configHandler, DatabaseHandler * dbHandler) : Stage()
{
    LabelStage::configHandler = configHandler;
    if (configHandler->getDatasetType() == "subset") {
        labeler = new Labeler(configHandler, dbHandler);
    } else if (configHandler->getDatasetType() == "full_set") {
        labeler = new LabelImporter(configHandler, dbHandler);
    }
}

void LabelStage::label()
{
    threadpool->start(labeler);
}
