#ifndef STAGE1_H
#define STAGE1_H

#include <QObject>
#include <QThreadPool>

class Stage1 : public QObject
{
    Q_OBJECT

public:
    Stage1();

protected:
    QThreadPool * threadpool = new QThreadPool();
};

#endif // STAGE1_H
