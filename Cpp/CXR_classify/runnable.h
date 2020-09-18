#ifndef RUNNABLE_H
#define RUNNABLE_H

#include <QObject>
#include <QRunnable>
#include <confighandler.h>
#include <databasehandler.h>
#include <expectedsizes.h>
#include <QString>
#include <QPixmap>

class Runnable: public QObject, public QRunnable
{
    Q_OBJECT
public:
    Runnable(ConfigHandler *, DatabaseHandler * = nullptr);

protected:
    ConfigHandler * configHandler;
    DatabaseHandler * dbHandler;
    quint64 expected_size;
    quint64 expected_num_files;

signals:
    void finished();
    void attemptUpdateProBarValue(quint64);
    void attemptUpdateProBarBounds(quint64, quint64);
    void attemptUpdateText(QString);
    void attemptUpdateImage(QPixmap);
};

#endif // RUNNABLE_H
