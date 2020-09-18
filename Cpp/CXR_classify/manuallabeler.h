#ifndef LABELER_H
#define LABELER_H

#include <QObject>
#include <pqxx/pqxx>
#include <dcmtk/dcmimgle/dcmimage.h>
#include <dcmtk/dcmdata/dcfilefo.h>
#include <string>
#include "opencv2/imgproc.hpp"
#include "confighandler.h"
#include "databasehandler.h"
#include "runnable.h"

class ManualLabeler : public Runnable
{
    Q_OBJECT // This Q_OBJECT is necessary for the MOC compilation
public:
    ManualLabeler(ConfigHandler *, DatabaseHandler *);

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
