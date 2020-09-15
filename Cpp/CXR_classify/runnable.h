#ifndef RUNNABLE_H
#define RUNNABLE_H

#include <QRunnable>
#include <signals.h>
#include <confighandler.h>
#include <databasehandler.h>
#include <expectedsizes.h>

class Runnable: QRunnable
{
public:
    Runnable(ConfigHandler * configHandler, DatabaseHandler * dbHandler);

protected:
    Signals * signalOptions;
    ConfigHandler * configHandler;
    DatabaseHandler * dbHandler;
    quint64 expected_size;
    quint64 expected_num_files;

};

#endif // RUNNABLE_H
