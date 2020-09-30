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

    void prepConfigIni();

    void setUrl(std::string);
    void setParentFolder();
    void setCsvPath();
    void setColumnsInfoPath();

    boost::property_tree::ptree getDbInfo();
    std::string getTableName(std::string);
    std::string getUrl();
    std::string getTgzFilename();
    std::string getDatasetName();
    std::string getColumnsInfoPath();
    std::string getCsvPath();
    std::string getDatasetType();
    std::string getParentFolder();

private:
    std::string configFilename;
    boost::property_tree::ptree configFile;

    boost::property_tree::ptree getSection(std::string);
    std::string getSetting(std::string, std::string);
    void setSetting(std::string, std::string, std::string);
};

#endif // CONFIGHANDLERS_H
