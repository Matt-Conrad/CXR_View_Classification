#ifndef CONFIGHANDLERS_H
#define CONFIGHANDLERS_H

#include <string>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/ini_parser.hpp>

class ConfigHandler
{
public:
    ConfigHandler(std::string);
    ~ConfigHandler();
    boost::property_tree::ptree getSection(std::string);
    std::string getSetting(std::string, std::string);
    void setSetting(std::string, std::string, std::string);

private:
    std::string configFilename;
    boost::property_tree::ptree configFile;
};

#endif // CONFIGHANDLERS_H
