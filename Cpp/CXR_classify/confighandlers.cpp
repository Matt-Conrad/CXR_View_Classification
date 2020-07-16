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
}

void ConfigHandler::setUrl(std::string url)
{
    setSetting("misc", "url", url);
}

boost::property_tree::ptree ConfigHandler::getDbInfo()
{
    return getSection("postgresql");
}

std::string ConfigHandler::getTableName(std::string table)
{
    return getSetting("table_names", table);
}

std::string ConfigHandler::getUrl()
{
    return getSetting("misc", "url");
}

std::string ConfigHandler::getTgzFilename()
{
    return getUrl().substr(getUrl().find_last_of("/") + 1);
}

std::string ConfigHandler::getDatasetName()
{
    return getTgzFilename().substr(0, getTgzFilename().find_last_of("."));
}

std::string ConfigHandler::getColumnsInfoPath()
{
    return getSetting("misc", "columns_info_relative_path");
}

std::string ConfigHandler::getCsvPath()
{
    return getSetting("misc", "csv_relative_path");
}

std::string ConfigHandler::getDatasetType()
{
    return getSetting("dataset_info", "dataset");
}



