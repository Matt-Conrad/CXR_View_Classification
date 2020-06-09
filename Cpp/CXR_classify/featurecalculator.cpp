#include "featurecalculator.h"

FeatureCalculator::FeatureCalculator(std::string columnsInfo, std::string configFilename, std::string sectionName, std::string folderFullPath) : QObject()
{
    FeatureCalculator::columnsInfo = columnsInfo;
    FeatureCalculator::configFilename = configFilename;
    FeatureCalculator::sectionName = sectionName;
    FeatureCalculator::folderFullPath = folderFullPath;

    FeatureCalculator::host = configParser(configFilename, "postgresql").get<std::string>("host");
    FeatureCalculator::port = configParser(configFilename, "postgresql").get<std::string>("port");
    FeatureCalculator::database = configParser(configFilename, "postgresql").get<std::string>("database");
    FeatureCalculator::user = configParser(configFilename, "postgresql").get<std::string>("user");
    FeatureCalculator::password = configParser(configFilename, "postgresql").get<std::string>("password");

    FeatureCalculator::metadataTableName = configParser(configFilename, "table_info").get<std::string>("metadata_table_name");
    FeatureCalculator::featTableName = configParser(configFilename, "table_info").get<std::string>("features_table_name");
}

void FeatureCalculator::calculateFeatures()
{
    addTableToDb();

    try
    {
        // Connect to the database
        pqxx::connection c("host=" + host + " port=" + port + " dbname=" + database + " user=" + user + " password=" + password);

        // Start a transaction
        pqxx::work w(c);

        // Execute query
        pqxx::result r = w.exec("SELECT * FROM " + metadataTableName + ";");

        quint64 count = 0;
        for (int rownum=0; rownum < r.size(); ++rownum)
        {
            std::this_thread::sleep_for (std::chrono::seconds(1));
            const pqxx::row row = r[rownum];
            const char * filePath = row["file_path"].c_str();
            count++;

            DicomImage * dcmImage = new DicomImage(filePath);
            uint16_t * pixelData = (uint16_t *) (dcmImage->getOutputData(16));

            uint64_t height = dcmImage->getHeight();
            uint64_t width = dcmImage->getWidth();

            cv::Mat originalImage(height, width, CV_16U, pixelData);

            DcmFileFormat file_format;
            file_format.loadFile(filePath);

            DcmTagKey photometricKey(40, 4); // photometric interpretation
            OFString photometricValue;
            file_format.getDataset()->findAndGetOFString(photometricKey, photometricValue);

            cv::Mat preprocessedImage = preprocessing(originalImage, photometricValue.c_str());

            cv::Mat horProfile = calcHorProf(preprocessedImage, 200, 200);
            cv::Mat vertProfile = calcVertProf(preprocessedImage, 200, 200);

            store(filePath, horProfile, vertProfile);

            delete dcmImage;
        }

        w.commit();
    }
    catch (std::exception const &e)
    {
        std::cerr << e.what() << std::endl;
    }

    emit finished();
}

void FeatureCalculator::store(std::string filePath, cv::Mat horProfile, cv::Mat vertProfile)
{
    try
    {
        // Connect to the database
        pqxx::connection c("host=" + host + " port=" + port + " dbname=" + database + " user=" + user + " password=" + password);

        // Create SQL query
        std::vector<float> horVec(horProfile.begin<float>(), horProfile.end<float>());
        std::vector<float> vertVec(vertProfile.begin<float>(), vertProfile.end<float>());

        std::vector<std::string> horVecString(horVec.size());
        std::transform(horVec.begin(), horVec.end(), horVecString.begin(), [](const float& val)
        {
            return std::to_string(val);
        });

        std::vector<std::string> vertVecString(vertVec.size());
        std::transform(vertVec.begin(), vertVec.end(), vertVecString.begin(), [](const float& val)
        {
            return std::to_string(val);
        });

        std::string sqlQuery = "INSERT INTO " + featTableName + " (file_name, file_path, hor_profile, vert_profile) VALUES ('" +
                filePath.substr(filePath.find_last_of("/") + 1) + "', '" + filePath + "', '{" + boost::algorithm::join(horVecString, ", ") +
                "}', '{" + boost::algorithm::join(vertVecString, ", ") + "}');";

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

cv::Mat FeatureCalculator::calcHorProf(cv::Mat image, unsigned width, unsigned height)
{
    cv::Mat imageSquare(height, width, CV_32F);
    cv::resize(image, imageSquare, cv::Size(width, height), 0, 0, cv::INTER_AREA);
    \
    cv::Mat horProfile(height, width, CV_32F);
    cv::reduce(imageSquare, horProfile, 0, cv::REDUCE_AVG, CV_32F);

    return horProfile;
}

cv::Mat FeatureCalculator::calcVertProf(cv::Mat image, unsigned width, unsigned height)
{
    cv::Mat imageSquare(height, width, CV_32F);
    cv::resize(image, imageSquare, cv::Size(width, height), 0, 0, cv::INTER_AREA);

    cv::Mat vertProfile(height, width, CV_32F);
    cv::reduce(imageSquare, vertProfile, 0, cv::REDUCE_AVG, CV_32F);

    return vertProfile;
}

cv::Mat FeatureCalculator::preprocessing(cv::Mat image, std::string photometric)
{
    double highestPossibleIntensity = 65536;
    cv::Mat imageDouble(image.rows, image.cols, CV_64F);
    image.convertTo(imageDouble, CV_64F);
    cv::Mat imageNorm(image.rows, image.cols, CV_64F);
    imageNorm = imageDouble / highestPossibleIntensity;

    if (photometric == "MONOCHROME1") {
        imageNorm = 1.0 - imageNorm;
    }

    // Create histogram
    unsigned histogram[65536] = {};
    for (auto j = 0; j < imageNorm.rows; j++) {
        for (auto i = 0; i < imageNorm.cols; i++) {
            ++histogram[(unsigned) (imageNorm.at<double>(j,i) * 65535)];
        }
    }

    // Get 1st percentile
    int sum = 0;
    int index = 0;
    while (sum < 0.01 * imageNorm.rows * imageNorm.cols) {
        sum += histogram[index];
        index++;
    }

    double firstPercentile = index/65535.0;

    // Get median
    sum = 0;
    index = 0;
    while (sum < 0.50 * imageNorm.rows * imageNorm.cols) {
        sum += histogram[index];
        index++;
    }

    double median = index/65535.0;

    // Get 99th percentile
    sum = 0;
    index = 65535;
    while (sum < 0.01 * imageNorm.rows * imageNorm.cols) {
        sum += histogram[index];
        index--;
    }

    double nineninePercentile = index/65535.0;

    cv::Mat enhancedImage(imageNorm.rows, imageNorm.cols, CV_64F);
    // Contrast stretch
    for (auto j = 0; j < imageNorm.rows; j++) {
        for (auto i = 0; i < imageNorm.cols; i++) {
//            double intensity = imageNorm.at<double>(j,i);
            if (imageNorm.at<double>(j,i) < firstPercentile) {
                enhancedImage.at<double>(j,i) = 0.0;
            } else if (imageNorm.at<double>(j,i) > nineninePercentile) {
                enhancedImage.at<double>(j,i) = 1.0;
            } else {
                enhancedImage.at<double>(j,i) = (imageNorm.at<double>(j,i) - firstPercentile) / (nineninePercentile - firstPercentile) * 1.0;
            }
        }
    }

    cv::Mat enhancedImageFloat(image.rows, image.cols, CV_32F);
    enhancedImage.convertTo(enhancedImageFloat, CV_32F);

    cv::Mat imageBinarized(image.rows, image.cols, CV_32F);
    cv::threshold(enhancedImageFloat, imageBinarized, median, 1.0, cv::THRESH_BINARY);

    // vector with all non-black point positions
    std::vector<cv::Point> nonBlackList;
    nonBlackList.reserve(imageBinarized.rows * imageBinarized.cols);

    // add all non-black points to the vector
    for(int j = 0; j < imageBinarized.rows; ++j) {
        for(int i = 0; i < imageBinarized.cols; ++i) {
            // if not black: add to the list
            if(imageBinarized.at<float>(j,i) != 1.0) {
                nonBlackList.push_back(cv::Point(i,j));
            }
        }
    }

    // create bounding rect around those points
    cv::Rect bb = cv::boundingRect(nonBlackList);

    cv::Mat imageCropped = imageBinarized(bb);

    float scalePercent = 0.5;
    unsigned width = imageCropped.cols * scalePercent;
    unsigned height = imageCropped.rows * scalePercent;

    cv::Mat imageDownsize(height, width, CV_32F);

    cv::resize(imageCropped, imageDownsize, cv::Size(width, height), 0.5, 0.5, cv::INTER_AREA);

//    cv::namedWindow("image", cv::WINDOW_NORMAL);
//    cv::imshow("image", imageDownsize);
//    cv::waitKey(0);

    return imageDownsize;
}

void FeatureCalculator::addTableToDb()
{
    boost::property_tree::ptree columnsJson;
    boost::property_tree::read_json(columnsInfo, columnsJson);
    boost::property_tree::ptree elements = columnsJson.get_child("features_list");

    std::string sqlQuery = "CREATE TABLE " + featTableName + " (file_name VARCHAR(255) PRIMARY KEY, file_path VARCHAR(255)";

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





