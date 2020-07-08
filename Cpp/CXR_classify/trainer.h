#ifndef TRAINER_H
#define TRAINER_H

#include <QObject>
#include <pqxx/pqxx>
#include <pqxx/array.hxx>
#include <iostream>
#include <mlpack/core.hpp>
#include "mlpack/methods/linear_svm/linear_svm.hpp"
#include "mlpack/core/cv/k_fold_cv.hpp"
#include "mlpack/core/data/split_data.hpp"
#include "mlpack/core/cv/metrics/accuracy.hpp"
#include "confighandlers.h"
#include "unpacker.h"
#include "basicDbOps.h"

class Trainer : public QObject
{
    Q_OBJECT
public:
    Trainer(std::string, std::string, std::string, std::string);

public slots:
    void trainClassifier();

private:
    std::string featTableName;
    std::string labelTableName;

    boost::property_tree::ptree dbInfo;

    quint64 expected_num_files;

signals:
    void finished();
    void attemptUpdateText(QString);
};

#endif // TRAINER_H
