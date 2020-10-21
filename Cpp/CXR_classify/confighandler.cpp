#include "confighandler.h"

namespace fs = std::filesystem;

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
    setCsvName();
    setColumnsInfoName();
}

void ConfigHandler::readConfigFile()
{
    if (fs::exists(configFilename)) {
        boost::property_tree::ini_parser::read_ini(configFilename, configFile);
    }
}

void ConfigHandler::setUrl(std::string url)
{
    setSetting("misc", "url", url);
}

void ConfigHandler::setParentFolder()
{
    setSetting("misc", "parent_folder", fs::current_path());
}

void ConfigHandler::setCsvName()
{
    setSetting("misc", "csv_filename", "image_labels.csv");
}

void ConfigHandler::setColumnsInfoName()
{
    setSetting("misc", "columns_info_name", "columns_info.json");
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

std::string ConfigHandler::getTgzFilePath()
{
    return prependParentPath(fs::path(getTgzFilename()));
}

std::string ConfigHandler::getDatasetName()
{
    return getTgzFilename().substr(0, getTgzFilename().find_last_of("."));
}

std::string ConfigHandler::getUnpackFolderPath()
{
    return prependParentPath(fs::path(getDatasetName()));
}

std::string ConfigHandler::getColumnsInfoName()
{
    return getSetting("misc", "columns_info_name");
}

std::string ConfigHandler::getColumnsInfoPath()
{
    return prependParentPath(fs::path(getCsvName()));
}

std::string ConfigHandler::getCsvName()
{
    return getSetting("misc", "csv_filename");
}

std::string ConfigHandler::getCsvPath()
{
    return prependParentPath(getCsvName());
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

std::string ConfigHandler::getConfigFilePath()
{
    return prependParentPath(getConfigFilename());
}

std::string ConfigHandler::prependParentPath(std::string fsItem)
{
    return (fs::path(getParentFolder()) / fs::path(fsItem));
}
