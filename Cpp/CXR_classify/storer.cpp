#include "storer.h"
#include <chrono>

Storer::Storer(ConfigHandler * configHandler, DatabaseHandler * dbHandler) : Stage(configHandler, dbHandler)
{

}

void Storer::dicomToDb()
{
    auto start = std::chrono::high_resolution_clock::now();
    emit attemptUpdateText("Storing metadata");
    emit attemptUpdateProBarBounds(0, expected_num_files);

    std::string metadataTableName = configHandler->getTableName("metadata");
    std::string columnsInfoPath = configHandler->getColumnsInfoPath();

    // Create table if it isn't already there
    if (!dbHandler->tableExists(metadataTableName)) {
        dbHandler->addTableToDb(columnsInfoPath, "elements", metadataTableName);
    }

    emit attemptUpdateProBarValue(0);

    // Open the json with the list of elements we're interested in
    boost::property_tree::ptree columnsJson;
    boost::property_tree::read_json(columnsInfoPath, columnsJson);
    boost::property_tree::ptree elements = columnsJson.get_child("elements");

    quint64 storeCount = 0;
    for (auto & p : std::filesystem::recursive_directory_iterator("./" + configHandler->getDatasetName())) {
        if (p.path().extension() == ".dcm") {
            try
            {
                // Create SQL query
                std::string sqlQuery = createSqlQuery(metadataTableName, elements, p.path().string());

                // Start a transaction
                pqxx::work w(*(dbHandler->getInputConnection()));

                // Execute query
                pqxx::result r = w.exec(sqlQuery);

                w.commit();

                storeCount++;
                emit attemptUpdateProBarValue(storeCount);
            }
            catch (std::exception const &e)
            {
              std::cerr << e.what() << std::endl;
            }
        }
    }
    emit attemptUpdateText("Done storing metadata");
    emit finished();
    auto finish = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed = finish - start;
    std::cout << "Elapsed time: " << elapsed.count() << " s\n";
}

std::string Storer::createSqlQuery(std::string tableName, boost::property_tree::ptree elements, std::string filePath)
{
    // Read file
    DcmFileFormat file_format;
    OFCondition status = file_format.loadFile(filePath.c_str());

    // Go through the list of elements and try to read the value
    for (boost::property_tree::ptree::value_type & element : elements) {
        // Get tag and separate into its parts
        std::string tag = element.second.get<std::string>("tag");
        std::string groupNameString;
        std::string elementNumString;

        tag.erase(std::remove_if(tag.begin(), tag.end(), ::isspace), tag.end()); // Remove blank spaces
        std::istringstream tagStream(tag);
        getline(tagStream, groupNameString, ',');
        getline(tagStream, elementNumString, ',');

        uint16_t groupNameInt = std::stoul(groupNameString, nullptr, 16);
        uint16_t elementNumInt = std::stoul(elementNumString, nullptr, 16);

        DcmTagKey tagKey(groupNameInt, elementNumInt);
        OFString tagValue;
        file_format.getDataset()->findAndGetOFString(tagKey, tagValue);

        if (tagValue != "") {
            if (element.second.get<std::string>("db_datatype").find("INT") != std::string::npos) {
                element.second.put("value", tagValue.c_str());
            } else if (element.second.get<std::string>("db_datatype").find("CHAR") != std::string::npos) {
                std::string str(tagValue.c_str());
                element.second.put("value", "'" + str + "'");
            }
        } else {
            element.second.put("value", "NULL");
        }
    }

    std::vector<std::string> names{"file_name", "file_path"};
    std::vector<std::string> values{"'" + filePath.substr(filePath.find_last_of("/") + 1) + "'", "'" + filePath + "'"};

    for (boost::property_tree::ptree::value_type & element : elements) {
        if (!element.second.get<bool>("calculation_only")) {
            names.push_back(element.first);
            values.push_back(element.second.get<std::string>("value"));
        }
    }

    std::string sqlQuery = "INSERT INTO " + tableName + " (" + boost::algorithm::join(names, ", ") + ") VALUES (" + boost::algorithm::join(values, ", ") + ");";

    return sqlQuery;
}
