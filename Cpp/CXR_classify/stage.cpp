#include "stage.h"

Stage::Stage(ConfigHandler * configHandler) : QObject()
{
    Stage::configHandler = configHandler;
    Stage::expected_num_files = expected_num_files_in_dataset.at(configHandler->getTgzFilename());
    Stage::expected_size = expected_sizes.at(configHandler->getTgzFilename());
}
