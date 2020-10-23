#ifndef CONFIGHANDLERS_H
#define CONFIGHANDLERS_H

#include <string>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/ini_parser.hpp>
#include <boost/dll/runtime_symbol_info.hpp>
#include <filesystem>
#include "expectedsizes.h"

class ConfigHandler
{
public:
    ConfigHandler(std::string);
    ~ConfigHandler();

    boost::property_tree::ptree getDbInfo();
    std::string getTableName(std::string);
    std::string getUrl();
    std::string getTgzFilename();
    std::string getTgzFilePath();
    std::string getDatasetName();
    std::string getUnpackFolderPath();
    std::string getColumnsInfoName();
    std::string getColumnsInfoPath();
    std::string getCsvName();
    std::string getCsvPath();
    std::string getDatasetType();
    std::string getParentFolder();
    std::string getLogLevel();
    std::string getConfigFilename();
    std::string getConfigFilePath();
    std::string prependParentPath(std::string);

private:
    std::string configFilename;
    boost::property_tree::ptree configFile;

    boost::property_tree::ptree getSection(std::string);
    std::string getSetting(std::string, std::string);
    void setSetting(std::string, std::string, std::string);

    void prepConfigIni();

    void setUrl(std::string);
    void setParentFolder();
    void setCsvName();
    void setColumnsInfoName();

    void readConfigFile();
};

#endif // CONFIGHANDLERS_H
