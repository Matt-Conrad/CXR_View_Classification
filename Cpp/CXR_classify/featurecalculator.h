#ifndef FEATURECALCULATOR_H
#define FEATURECALCULATOR_H

#include <pqxx/pqxx>
#include <boost/algorithm/string/join.hpp>
#include <dcmtk/dcmimgle/dcmimage.h>
#include <dcmtk/dcmdata/dcfilefo.h>
#include <vector>
#include <thread>
#include "opencv2/imgproc.hpp"
#include <opencv2/cudaarithm.hpp>
#include "confighandler.h"
#include "databasehandler.h"
#include "runnable.h"

class FeatureCalculator : public Runnable
{
public:
    FeatureCalculator(ConfigHandler *, DatabaseHandler *);

public slots:
    void run();

private:
    std::string featTableName;

    void store(std::string, cv::Mat, cv::Mat);
    void calculateFeatures(pqxx::row);
};

#endif // FEATURECALCULATOR_H
