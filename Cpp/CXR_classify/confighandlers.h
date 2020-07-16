#ifndef CONFIGHANDLERS_H
#define CONFIGHANDLERS_H

#include <string>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/ini_parser.hpp>
#include <boost/dll/runtime_symbol_info.hpp>

class ConfigHandler
{
public:
    ConfigHandler(std::string);
    ~ConfigHandler();

    void setUrl(std::string);

    boost::property_tree::ptree getDbInfo();
    std::string getTableName(std::string);
    std::string getParentFolder();
    std::string getUrl();
    std::string getTgzFilename();
    std::string getDatasetName();
    std::string getColumnsInfoPath();
    std::string getCsvPath();
    std::string getDatasetType();

    boost::property_tree::ptree getSection(std::string);
    std::string getSetting(std::string, std::string);
    void setSetting(std::string, std::string, std::string);

private:
    std::string configFilename;
    boost::property_tree::ptree configFile;
};

#endif // CONFIGHANDLERS_H
