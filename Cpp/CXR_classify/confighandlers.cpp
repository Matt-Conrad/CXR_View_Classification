
#include "confighandlers.h"

boost::property_tree::ptree config::getSection(std::string filename, std::string sectionName)
{
    boost::property_tree::ptree configFile;

    boost::property_tree::ini_parser::read_ini(filename, configFile);

    boost::property_tree::ptree section = configFile.get_child(sectionName);

    return section;
}
