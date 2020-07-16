#ifndef FEATURECALCULATOR_H
#define FEATURECALCULATOR_H

#include <QObject>
#include <QApplication>
#include <iostream>
#include <fstream>
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
#include <vector>
#include <assert.h>
#include "opencv2/opencv.hpp"
#include <opencv2/core/core.hpp>
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/core/types_c.h"
#include "opencv2/imgproc.hpp"
#include <opencv2/imgcodecs/imgcodecs.hpp>
#include "confighandlers.h"
#include "basicDbOps.h"
#include "unpacker.h"

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
