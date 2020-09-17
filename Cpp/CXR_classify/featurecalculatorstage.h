#ifndef FEATURECALCULATORSTAGE_H
#define FEATURECALCULATORSTAGE_H

#include <QObject>
#include "databasehandler.h"
#include "confighandler.h"
#include "stage.h"
#include "featurecalculator.h"

class FeatureCalculatorStage : public Stage
{
    Q_OBJECT
public:
    FeatureCalculatorStage(ConfigHandler *, DatabaseHandler *);
    FeatureCalculator * featureCalculator;

public slots:
    void calculateFeatures();
};

#endif // FEATURECALCULATORSTAGE_H
