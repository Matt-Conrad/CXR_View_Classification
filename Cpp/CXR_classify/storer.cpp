#include "storer.h"

Storer::Storer(std::string columnsInfo, std::string configFilename, std::string sectionName, std::string folderFullPath) : QObject()
{
    Storer::columnsInfo = columnsInfo;
    Storer::configFilename = configFilename;
    Storer::sectionName = sectionName;
    Storer::folderFullPath = folderFullPath;

    Storer::host = configParser(configFilename, "postgresql").get<std::string>("host");
    Storer::port = configParser(configFilename, "postgresql").get<std::string>("port");
    Storer::database = configParser(configFilename, "postgresql").get<std::string>("database");
    Storer::user = configParser(configFilename, "postgresql").get<std::string>("user");
    Storer::password = configParser(configFilename, "postgresql").get<std::string>("password");

    Storer::metadataTableName = configParser(configFilename, "table_info").get<std::string>("metadata_table_name");
}

void Storer::dicomToDb()
{
    // Create the database if it isn't already there
    if (!dbExists()){
        createNewDb();
    }

    // Create table if it isn't already there
    if (!tableExists(metadataTableName)) {
        addTableToDb();
    }

    // Open the json with the list of elements we're interested in
    boost::property_tree::ptree columnsJson;
    boost::property_tree::read_json(columnsInfo, columnsJson);
    boost::property_tree::ptree elements = columnsJson.get_child("elements");

    for (auto & p : std::filesystem::recursive_directory_iterator(folderFullPath)) {
        if (p.path().extension() == ".dcm") {
//            std::this_thread::sleep_for (std::chrono::seconds(1));
            try
            {
                // Connect to the database
                pqxx::connection c("host=" + host + " port=" + port + " dbname=" + database + " user=" + user + " password=" + password);

                // Create SQL query
                std::cout << p.path().string() << std::endl;
                std::string sqlQuery = createSqlQuery(metadataTableName, elements, p.path().string());

                // Start a transaction
                pqxx::work w(c);

                // Execute query
                pqxx::result r = w.exec(sqlQuery);

                w.commit();
            }
            catch (std::exception const &e)
            {
              std::cerr << e.what() << std::endl;
            }
        }
    }

    emit finished();
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

void Storer::addTableToDb()
{
    boost::property_tree::ptree columnsJson;
    boost::property_tree::read_json(columnsInfo, columnsJson);
    boost::property_tree::ptree elements = columnsJson.get_child("elements");

    std::string sqlQuery = "CREATE TABLE " + metadataTableName + " (file_name VARCHAR(255) PRIMARY KEY, file_path VARCHAR(255)";

    for (boost::property_tree::ptree::value_type & column : elements) {
        sqlQuery += (", " + column.first + " " + column.second.get<std::string>("db_datatype"));
    }
    sqlQuery += ");";

    try
    {
        // Connect to the database
        pqxx::connection c("host=" + host + " port=" + port + " dbname=" + database + " user=" + user + " password=" + password);

        // Start a transaction
        pqxx::nontransaction w(c);

        // Execute query
        pqxx::result r = w.exec(sqlQuery);

        // Commit your transaction
        w.commit();
    }
    catch (std::exception const &e)
    {
      std::cerr << e.what() << std::endl;
    }
}

bool Storer::tableExists(std::string tableName)
{
    try
    {
        // Connect to the database
        pqxx::connection c("host=" + host + " port=" + port + " dbname=" + database + " user=" + user + " password=" + password);

        // Start a transaction
        pqxx::work w(c);

        // Execute query
        pqxx::result r = w.exec("SELECT * FROM information_schema.tables WHERE table_name=\'" + tableName + "\';");

        // Return based on result
        if (r.size() == 0) {
            return false;
        } else {
            return true;
        }
    }
    catch (std::exception const &e)
    {
        return false;
    }
}

void Storer::createNewDb()
{
    try
    {
        // Connect to the database
        pqxx::connection c("host=" + host + " port=" + port + " dbname=postgres user=postgres password=postgres");

        // Start a transaction
        pqxx::nontransaction w(c);

        // Execute query
        pqxx::result r = w.exec("CREATE DATABASE " + database + ';');

        // Commit your transaction
        w.commit();
    }
    catch (std::exception const &e)
    {
      std::cerr << e.what() << std::endl;
    }
}

bool Storer::dbExists()
{
    try
    {
        // Connect to the database
        pqxx::connection c("host=" + host + " port=" + port + " dbname=postgres user=" + user + " password=" + password);

        // Start a transaction
        pqxx::work w(c);

        // Execute query
        pqxx::result r = w.exec("SELECT datname FROM pg_catalog.pg_database WHERE datname=\'" + database + "\'");

        // Return based on result
        if (r.size() == 0) {
            return false;
        } else {
            return true;
        }

    }
    catch (std::exception const &e)
    {
      std::cerr << e.what() << std::endl;
    }
}
