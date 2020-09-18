#include "runnable.h"

Runnable::Runnable(ConfigHandler * configHandler, DatabaseHandler * dbHandler): QObject(), QRunnable()
{
    Runnable::configHandler = configHandler;
    Runnable::dbHandler = dbHandler;
    Runnable::expected_num_files = expected_num_files_in_dataset.at(configHandler->getDatasetType());
    Runnable::expected_size = expected_sizes.at(configHandler->getDatasetType());
}
