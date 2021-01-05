#ifndef TRAINER_H
#define TRAINER_H

#include <pqxx/pqxx>
#include <pqxx/array.hxx>
#include <QtCore/QThreadPool>
#include <QtCore/QRunnable>
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

    QThreadPool * threadpool = new QThreadPool();
};

// These functions can be called from "C" 
extern "C" {
    Trainer * Trainer_new();
    void Trainer_run(Trainer *);
}

class TrainProcessor : public QRunnable
{
public:
    TrainProcessor(arma::mat, arma::Row<size_t>, int, std::vector<double> *, ConfigHandler *, DatabaseHandler *);

public slots:
    void run();

private:
    ConfigHandler * configHandler;
    DatabaseHandler * dbHandler;

    arma::mat xTrain;
    arma::Row<size_t> yTrain;
    int index;
    std::vector<double> * results;
};

#endif // TRAINER_H
