#include "labelstage.h"

LabelStage::LabelStage(ConfigHandler * configHandler, DatabaseHandler * dbHandler) : Stage()
{
    if (configHandler->getDatasetType() == "subset") {
        labeler = new ManualLabeler(configHandler, dbHandler);
    } else if (configHandler->getDatasetType() == "full_set") {
        labeler = new LabelImporter(configHandler, dbHandler);
    }
}

void LabelStage::label()
{
    threadpool->start(labeler);
}
