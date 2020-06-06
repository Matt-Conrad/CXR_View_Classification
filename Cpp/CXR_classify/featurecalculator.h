#ifndef FEATURECALCULATOR_H
#define FEATURECALCULATOR_H

#include <QObject>
#include <QApplication>
#include <iostream>
#include <filesystem>
#include <pqxx/pqxx>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <boost/algorithm/string/join.hpp>
#include <dcmtk/dcmimgle/dcmimage.h>
#include <dcmtk/dcmdata/dcfilefo.h>
#include <dcmtk/dcmdata/dcdeftag.h>
#include <thread>
#include <chrono>
#include <cmath>
#include "opencv2/opencv.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/core/types_c.h"
#include "opencv2/imgproc.hpp"
#include "confighandlers.h"

class FeatureCalculator : public QObject
{
    Q_OBJECT
public:
    FeatureCalculator(std::string, std::string, std::string, std::string);

public slots:
    void calculateFeatures();

private:
    std::string columnsInfo;
    std::string configFilename;
    std::string sectionName;
    std::string folderFullPath;

    std::string host;
    std::string port;
    std::string database;
    std::string user;
    std::string password;

    std::string metadataTableName;
    std::string featTableName;

    void addTableToDb();
    cv::Mat preprocessing(cv::Mat, std::string);
    cv::Mat calcHorProf(cv::Mat, unsigned, unsigned);
    cv::Mat calcVertProf(cv::Mat, unsigned, unsigned);
    void store(std::string, cv::Mat, cv::Mat);

signals:
    void finished();
};

#endif // FEATURECALCULATOR_H
