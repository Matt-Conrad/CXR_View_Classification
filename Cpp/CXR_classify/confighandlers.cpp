
#include "confighandlers.h"

ConfigHandler::ConfigHandler(std::string configFilename)
{
    ConfigHandler::configFilename = configFilename;
}

boost::property_tree::ptree ConfigHandler::getSection(std::string sectionName)
{
    boost::property_tree::ptree configFile;

    boost::property_tree::ini_parser::read_ini(configFilename, configFile);

    boost::property_tree::ptree section = configFile.get_child(sectionName);

    return section;
}

std::string ConfigHandler::getSetting(std::string sectionName, std::string settingName)
{
    boost::property_tree::ptree section = ConfigHandler::getSection(sectionName);
    return section.get<std::string>(settingName);
}
