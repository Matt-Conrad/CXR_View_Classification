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
#include "runnable.h"
#include <QThreadPool>

class Trainer : public Runnable
{
public:
    Trainer(ConfigHandler *, DatabaseHandler *);

public slots:
    void run();

private:
    QThreadPool * threadpool = new QThreadPool();
};


class TrainProcessor : public Runnable
{
public:
    TrainProcessor(arma::mat, arma::Row<size_t>, int, std::vector<double> *, ConfigHandler *, DatabaseHandler *);

public slots:
    void run();

private:
    arma::mat xTrain;
    arma::Row<size_t> yTrain;
    int index;
    std::vector<double> * results;
};

#endif // TRAINER_H
