#include "featurecalculatorstage.h"

FeatureCalculatorStage::FeatureCalculatorStage(ConfigHandler * configHandler, DatabaseHandler * dbHandler) : Stage1()
{
    featureCalculator = new FeatureCalculator(configHandler, dbHandler);
}

void FeatureCalculatorStage::calculateFeatures()
{
    threadpool->start(featureCalculator);
}
