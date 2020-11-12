#ifndef FEATURECALCULATOR_H
#define FEATURECALCULATOR_H

#include <pqxx/pqxx>
#include <boost/algorithm/string/join.hpp>
#include <dcmtk/dcmimgle/dcmimage.h>
#include <dcmtk/dcmdata/dcfilefo.h>
#include <vector>
#include <thread>
#include "opencv2/imgproc.hpp"
//#include <opencv2/cudaarithm.hpp>
#include "confighandler.h"
#include "databasehandler.h"
#include "runnable.h"
#include <QThreadPool>

class FeatureCalculator : public Runnable
{
public:
    FeatureCalculator(ConfigHandler *, DatabaseHandler *);

public slots:
    void run();

private:
    QThreadPool * threadpool = new QThreadPool();
    std::string featTableName;
};

class Processor : public Runnable
{
public:
    Processor(std::string, ConfigHandler *, DatabaseHandler *);

public slots:
    void run();

private:
    void store(std::string, cv::Mat, cv::Mat);
    std::string filePath;
};

#endif // FEATURECALCULATOR_H
