#ifndef TRAINER_H
#define TRAINER_H

#include <pqxx/pqxx>
#include <pqxx/array.hxx>
#include "mlpack/methods/linear_svm/linear_svm.hpp"
#include "mlpack/core/cv/k_fold_cv.hpp"
#include "mlpack/core/data/split_data.hpp"
#include "mlpack/core/cv/metrics/accuracy.hpp"
#include "confighandler.h"
#include "databasehandler.h"
#include "expectedsizes.h"

class Trainer
{
public:
    Trainer();
    void run();

private:
    ConfigHandler * configHandler = new ConfigHandler("config.ini");
    DatabaseHandler * dbHandler = new DatabaseHandler(configHandler);
};

// These functions can be called from "C" 
extern "C" {
    Trainer * Trainer_new();
    void Trainer_run(Trainer *);
}

#endif // TRAINER_H
