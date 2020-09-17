#ifndef UNPACKSTAGE_H
#define UNPACKSTAGE_H

#include <QObject>
#include "confighandler.h"
#include "unpacker.h"
#include "stage.h"

class UnpackStage : public Stage
{
    Q_OBJECT
public:
    UnpackStage(ConfigHandler *);
    Unpacker * unpacker;

public slots:
    void unpack();
};

#endif // UNPACKSTAGE_H
