
#include "confighandlers.h"

ConfigHandler::ConfigHandler(std::string configFilename)
{
    ConfigHandler::configFilename = configFilename;
    boost::property_tree::ini_parser::read_ini(configFilename, configFile);
}

ConfigHandler::~ConfigHandler()
{
    boost::property_tree::ini_parser::write_ini(configFilename, configFile);
}

boost::property_tree::ptree ConfigHandler::getSection(std::string sectionName)
{
    return configFile.get_child(sectionName);
}

std::string ConfigHandler::getSetting(std::string sectionName, std::string settingName)
{
    boost::property_tree::ptree section = ConfigHandler::getSection(sectionName);
    return section.get<std::string>(settingName);
}

void ConfigHandler::setSetting(std::string sectionName, std::string settingName, std::string value)
{
    configFile.put(sectionName + "." + settingName, value);
//    boost::property_tree::ini_parser::write_ini(configFilename, configFile);
}

