#include "confighandler.h"

ConfigHandler::ConfigHandler(std::string configFilename)
{
    ConfigHandler::configFilename = configFilename;
    readConfigFile();
    prepConfigIni();
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

void ConfigHandler::prepConfigIni()
{
    setUrl(sourceUrl.at(getDatasetType()));
    setParentFolder();
    setCsvPath();
    setColumnsInfoPath();
}

void ConfigHandler::readConfigFile()
{
    if (std::filesystem::exists(configFilename)) {
        boost::property_tree::ini_parser::read_ini(configFilename, configFile);
    }
}

void ConfigHandler::setUrl(std::string url)
{
    setSetting("misc", "url", url);
}

void ConfigHandler::setParentFolder()
{
    setSetting("misc", "parent_folder", std::filesystem::current_path());
}

void ConfigHandler::setCsvPath()
{
    setSetting("misc", "csv_relative_path", "../../miscellaneous/image_labels.csv");
}

void ConfigHandler::setColumnsInfoPath()
{
    setSetting("misc", "columns_info_relative_path", "../../miscellaneous/columns_info.json");
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

std::string ConfigHandler::getParentFolder()
{
    return getSetting("misc", "parent_folder");
}

std::string ConfigHandler::getLogLevel()
{
    return getSetting("logging", "level");
}

std::string ConfigHandler::getConfigFilename()
{
    return configFilename;
}
