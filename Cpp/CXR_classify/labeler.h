#ifndef LABELER_H
#define LABELER_H

#include <QObject>
#include <QWidget>
#include <QPushButton>
#include <QGridLayout>
#include <QLabel>
#include <pqxx/pqxx>
#include <dcmtk/dcmimgle/dcmimage.h>
#include <dcmtk/dcmdata/dcfilefo.h>
#include "opencv2/imgproc.hpp"
#include "confighandler.h"
#include "databasehandler.h"
#include "runnable.h"
#include <string>

class Labeler : public Runnable
{
    Q_OBJECT
public:
    Labeler(ConfigHandler *, DatabaseHandler *);

private:
    unsigned count = 0;

    std::string labelTableName;

    pqxx::result imageList;
    pqxx::result::const_iterator record;
    pqxx::connection * connection;

    void queryImageList();
    void displayNextImage();
    void storeLabel(std::string);

public slots:
    void run();
    void frontal();
    void lateral();
};

#endif // LABELER_H
