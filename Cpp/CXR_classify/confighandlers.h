#ifndef CONFIGHANDLERS_H
#define CONFIGHANDLERS_H

#include <string>
#include <unordered_map>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/ini_parser.hpp>

boost::property_tree::ptree configParser(std::string filename, std::string sectionName);

#endif // CONFIGHANDLERS_H
