#ifndef FEATURECALCULATORSTAGE_H
#define FEATURECALCULATORSTAGE_H

#include <QObject>
#include "databasehandler.h"
#include "confighandler.h"
#include "stage1.h"
#include "featurecalculator.h"

class FeatureCalculatorStage : public Stage1
{
    Q_OBJECT
public:
    FeatureCalculatorStage(ConfigHandler *, DatabaseHandler *);
    FeatureCalculator * featureCalculator;

public slots:
    void calculateFeatures();
};

#endif // FEATURECALCULATORSTAGE_H
