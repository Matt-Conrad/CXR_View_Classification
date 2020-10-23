#ifndef FEATURECALCULATOR_H
#define FEATURECALCULATOR_H

#include <pqxx/pqxx>
#include <boost/algorithm/string/join.hpp>
#include <dcmtk/dcmimgle/dcmimage.h>
#include <dcmtk/dcmdata/dcfilefo.h>
#include <vector>
#include "opencv2/imgproc.hpp"
// #include <opencv2/cudaarithm.hpp>
#include "confighandler.h"
#include "databasehandler.h"

class FeatureCalculator
{
public:
    FeatureCalculator();
    void run();

private:
    ConfigHandler * configHandler = new ConfigHandler("config.ini");
    DatabaseHandler * dbHandler = new DatabaseHandler(configHandler);

    std::string featTableName;

    cv::Mat imageUnsigned;
    cv::Mat imageFloat;
    cv::Mat imageResize;
    cv::Mat imageFloatFlat;
    cv::Mat horProfile;
    cv::Mat vertProfile;

    cv::Mat preprocessing(uint8_t);
    cv::Mat calcHorProf();
    cv::Mat calcVertProf();
    void store(std::string, cv::Mat, cv::Mat);
};

// These functions can be called from "C" 
extern "C" {
    FeatureCalculator * FeatureCalculator_new();
    void FeatureCalculator_run(FeatureCalculator *);
}

#endif // FEATURECALCULATOR_H
