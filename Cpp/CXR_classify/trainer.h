#ifndef TRAINER_H
#define TRAINER_H

#include <QObject>
#include <pqxx/pqxx>
#include <pqxx/array.hxx>
#include "mlpack/methods/linear_svm/linear_svm.hpp"
#include "mlpack/core/cv/k_fold_cv.hpp"
#include "mlpack/core/data/split_data.hpp"
#include "mlpack/core/cv/metrics/accuracy.hpp"
#include "confighandlers.h"
#include "basicDbOps.h"
#include "expectedsizes.h"

class Trainer : public QObject
{
    Q_OBJECT
public:
    Trainer(ConfigHandler *, DatabaseHandler *);

public slots:
    void trainClassifier();

private:
    quint64 expected_num_files;
    ConfigHandler * configHandler;
    DatabaseHandler * dbHandler;

signals:
    void finished();
    void attemptUpdateText(QString);
};

#endif // TRAINER_H
