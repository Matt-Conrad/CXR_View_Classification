#ifndef TRAINER_H
#define TRAINER_H

#include <QObject>
#include <pqxx/pqxx>
#include <pqxx/array.hxx>
#include "mlpack/methods/linear_svm/linear_svm.hpp"
#include "mlpack/core/cv/k_fold_cv.hpp"
#include "mlpack/core/data/split_data.hpp"
#include "mlpack/core/cv/metrics/accuracy.hpp"
#include "confighandler.h"
#include "databasehandler.h"
#include "stage.h"

class Trainer : public Stage
{
    Q_OBJECT

public:
    Trainer(ConfigHandler *, DatabaseHandler *);

public slots:
    void trainClassifier();
};

#endif // TRAINER_H
