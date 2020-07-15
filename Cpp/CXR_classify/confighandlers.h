#ifndef CONFIGHANDLERS_H
#define CONFIGHANDLERS_H

#include <string>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/ini_parser.hpp>

class ConfigHandler
{
public:
    ConfigHandler(std::string configFilename);
    boost::property_tree::ptree getSection(std::string sectionName);
    std::string getSetting(std::string sectionName, std::string settingName);

private:
    std::string configFilename;
};

#endif // CONFIGHANDLERS_H
