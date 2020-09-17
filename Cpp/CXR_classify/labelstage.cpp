#include "labelstage.h"

LabelStage::LabelStage(ConfigHandler * configHandler, DatabaseHandler * dbHandler) : Stage1()
{
//    if (configHandler->getDatasetType() == "subset") {
//        labeler = ManualLabeler
//    } else if (configHandler->getDatasetType() == "full_set") {
//        labeler = LabelImporter
//    }
    labeler = new Labeler(configHandler, dbHandler);
}

void LabelStage::label()
{
    threadpool->start(labeler);
}
