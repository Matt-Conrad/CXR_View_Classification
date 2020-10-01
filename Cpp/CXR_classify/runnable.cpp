#include "runnable.h"

Runnable::Runnable(ConfigHandler * configHandler, DatabaseHandler * dbHandler): QObject(), QRunnable()
{
    Runnable::configHandler = configHandler;
    Runnable::dbHandler = dbHandler;
    logger = spdlog::get(loggerName);
    expected_num_files = expected_num_files_in_dataset.at(configHandler->getDatasetType());
    expected_size = expected_sizes.at(configHandler->getDatasetType());
}
