#ifndef STAGE_H
#define STAGE_H

#include <QObject>
#include "expectedsizes.h"
#include "confighandlers.h"

class Stage : public QObject
{
    Q_OBJECT

public:
    Stage(ConfigHandler *);

protected:
    ConfigHandler * configHandler;
    quint64 expected_size;
    quint64 expected_num_files;

signals:
    void finished();
    void attemptUpdateProBarValue(quint64);
    void attemptUpdateProBarBounds(quint64, quint64);
    void attemptUpdateText(QString);
};

#endif // STAGE_H
