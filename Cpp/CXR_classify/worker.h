#ifndef WORKER_H
#define WORKER_H

#include <QRunnable>
#include <QObject>

//class Worker : public QRunnable
//{
//    Q_OBJECT
//public:
//    Worker(void (*fun_ptr) ());
//    void run();

//private:
//    void (*fun_ptr) ();

//};

class AppController;

class Worker : public QObject
{
    Q_OBJECT
public:
    Worker(AppController * controller);
    ~Worker();
public slots:
    void process();
signals:
    void finished();
    void error(QString err);
private:
    AppController * controller;
};


#endif // WORKER_H
