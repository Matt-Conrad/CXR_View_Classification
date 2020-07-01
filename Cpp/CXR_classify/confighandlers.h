#ifndef CONFIGHANDLERS_H
#define CONFIGHANDLERS_H

#include <string>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/ini_parser.hpp>

namespace config {
    boost::property_tree::ptree getSection(std::string filename, std::string sectionName);
}

#endif // CONFIGHANDLERS_H
