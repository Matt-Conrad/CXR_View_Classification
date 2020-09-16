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
#include "runnable.h"

class Trainer : public Runnable
{
public:
    Trainer(ConfigHandler *, DatabaseHandler *);

public slots:
    void run();

private:
    static const unsigned numSamples = 10;//7468;
};

#endif // TRAINER_H
