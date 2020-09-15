#include "appcontroller.h"

AppController::AppController()
{
    std::string url = c_sourceUrl.at(configHandler->getDatasetType());
    configHandler->setUrl(url);
}

AppController::~AppController()
{
    configHandler->~ConfigHandler();
}
