#ifndef FEATURECALCULATOR_H
#define FEATURECALCULATOR_H

#include <QObject>
#include <pqxx/pqxx>
#include <boost/algorithm/string/join.hpp>
#include <dcmtk/dcmimgle/dcmimage.h>
#include <dcmtk/dcmdata/dcfilefo.h>
#include <vector>
#include "opencv2/imgproc.hpp"
#include "confighandlers.h"
#include "basicDbOps.h"
#include "expectedsizes.h"

class FeatureCalculator : public QObject
{
    Q_OBJECT
public:
    FeatureCalculator(ConfigHandler *, DatabaseHandler *);

public slots:
    void calculateFeatures();

private:
    quint64 expected_num_files;

    ConfigHandler * configHandler;
    DatabaseHandler * dbHandler;

    std::string featTableName;

    cv::Mat preprocessing(cv::Mat, std::string, uint8_t);
    cv::Mat calcHorProf(cv::Mat, unsigned, unsigned);
    cv::Mat calcVertProf(cv::Mat, unsigned, unsigned);
    void store(std::string, cv::Mat, cv::Mat);

signals:
    void finished();
    void attemptUpdateProBarValue(quint64);
    void attemptUpdateProBarBounds(quint64, quint64);
    void attemptUpdateText(QString);
};

#endif // FEATURECALCULATOR_H
