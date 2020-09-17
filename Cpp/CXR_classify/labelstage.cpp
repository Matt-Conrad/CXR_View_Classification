#include "labelstage.h"

LabelStage::LabelStage(ConfigHandler * configHandler, DatabaseHandler * dbHandler) : Stage()
{
    LabelStage::configHandler = configHandler;
    labeler = new Labeler(configHandler, dbHandler);
    labelImporter = new LabelImporter(configHandler, dbHandler);
}

void LabelStage::label()
{
    if (configHandler->getDatasetType() == "subset") {
        threadpool->start(labeler);
    } else if (configHandler->getDatasetType() == "full_set") {
        threadpool->start(labelImporter);
    }
}
