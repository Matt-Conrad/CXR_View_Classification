#ifndef STAGE_H
#define STAGE_H

#include <QObject>
#include <QThreadPool>

class Stage : public QObject
{
    Q_OBJECT

public:
    Stage();

protected:
    QThreadPool * threadpool = new QThreadPool();
};

#endif // STAGE_H
