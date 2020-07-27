#ifndef FEATURECALCULATOR_H
#define FEATURECALCULATOR_H

#include <QObject>
#include <pqxx/pqxx>
#include <boost/algorithm/string/join.hpp>
#include <dcmtk/dcmimgle/dcmimage.h>
#include <dcmtk/dcmdata/dcfilefo.h>
#include <vector>
#include "opencv2/imgproc.hpp"
#include "confighandler.h"
#include "databasehandler.h"
#include "stage.h"

class FeatureCalculator : public Stage
{
    Q_OBJECT
public:
    FeatureCalculator(ConfigHandler *, DatabaseHandler *);

public slots:
    void calculateFeatures();

private:
    std::string featTableName;

    cv::Mat preprocessing(cv::Mat, uint8_t);
    cv::Mat calcHorProf(cv::Mat, unsigned, unsigned);
    cv::Mat calcVertProf(cv::Mat, unsigned, unsigned);
    void store(std::string, cv::Mat, cv::Mat);
};

#endif // FEATURECALCULATOR_H
