#ifndef LABELER_H
#define LABELER_H

#include <QObject>
#include <QWidget>
#include <QPushButton>
#include <QGridLayout>
#include <QLabel>
#include <iostream>
#include <pqxx/pqxx>
#include <dcmtk/dcmimgle/dcmimage.h>
#include <dcmtk/dcmdata/dcfilefo.h>
#include <dcmtk/dcmdata/dcdeftag.h>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <boost/algorithm/string/join.hpp>
#include "opencv2/opencv.hpp"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/core/types_c.h"
#include "opencv2/imgproc.hpp"
#include "confighandlers.h"

class Labeler : public QWidget
{
    Q_OBJECT
public:
    Labeler(std::string, std::string);

private:
    unsigned count = 0;
    std::string configFilename;
    std::string columnsInfo;
    std::string labelTableName;

    std::string host;
    std::string port;
    std::string database;
    std::string user;
    std::string password;

    pqxx::result imageList;
    pqxx::result::const_iterator record;
    pqxx::connection * connection;

    QLabel * label = new QLabel(this);
    QLabel * image = new QLabel(this);
    QPushButton * frontalButton = new QPushButton("Frontal", this);
    QPushButton * lateralButton = new QPushButton("Lateral", this);

    void queryImageList();
    void displayNextImage();
    void storeLabel(std::string);
    void addTableToDb();
    void closeLabelApp();
    void closeConnection();

private slots:
    void frontal();
    void lateral();

public slots:
    void fillWindow();

signals:
    void finished();
    void attemptUpdateText(QString);
};

#endif // LABELER_H
