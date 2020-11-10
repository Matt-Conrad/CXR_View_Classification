#include "featurecalculator.h"

#include <chrono>
#include <iostream>

FeatureCalculator::FeatureCalculator(ConfigHandler * configHandler, DatabaseHandler * dbHandler) : Runnable(configHandler, dbHandler)
{
    FeatureCalculator::featTableName = configHandler->getTableName("features");
}

void FeatureCalculator::run()
{
    std::chrono::steady_clock::time_point begin = std::chrono::steady_clock::now();
    logger->info("Calculating features from images");

    emit attemptUpdateText("Calculating features");
    emit attemptUpdateProBarBounds(0, expected_num_files);

    dbHandler->addTableToDb(configHandler->getColumnsInfoName(), "features_list", featTableName);

    emit attemptUpdateProBarValue(0);

    pqxx::result result = dbHandler->executeQuery(dbHandler->connection, "SELECT * FROM " + configHandler->getTableName("metadata") + ";");

    for (int rownum=0; rownum < result.size(); ++rownum){
        pqxx::row row = result[rownum];
        std::string filePath = row["file_path"].c_str();
        Processor * processor = new Processor(filePath, configHandler, dbHandler);
        threadpool->start(processor);
    }

    threadpool->waitForDone();

    std::chrono::steady_clock::time_point end = std::chrono::steady_clock::now();
    std::cout << "Time difference = " << (std::chrono::duration_cast<std::chrono::nanoseconds> (end - begin).count())/1000000000.0 << "[s]" << std::endl;
    logger->info("Done calculating features from images");
    emit attemptUpdateText("Done calculating features");
    emit attemptUpdateProBarValue(dbHandler->countRecords(featTableName));
    emit finished();
}


Processor::Processor(std::string filePath, ConfigHandler * configHandler, DatabaseHandler * dbHandler) : Runnable(configHandler, dbHandler)
{
    Processor::filePath = filePath;
}

void Processor::run()
{
//    std::cout << filePath << std::endl;
    DicomImage * dcmImage = new DicomImage(filePath.c_str());
    uint16_t * pixelData = (uint16_t *) (dcmImage->getOutputData(16)); // This scales the pixel values so that the intensity range is 0 - 2^16 instead of 0 - 2^bits_stored

    // Convert the image from uint16 to double
    uint64_t height = dcmImage->getHeight();
    uint64_t width = dcmImage->getWidth();

    cv::Mat imageUnsigned = cv::Mat(height, width, CV_16U, pixelData);
    cv::Mat imageFloat;
    imageUnsigned.convertTo(imageFloat, CV_64F);

    // Get the bits_stored for scaling intensities back down from 16 bits to their bits_stored value
    DcmFileFormat file_format;
    file_format.loadFile(filePath.c_str());

    DcmTagKey bitsStoredKey(40, 257); // bits stored
    OFString bitsStoredValue;
    file_format.getDataset()->findAndGetOFString(bitsStoredKey, bitsStoredValue);

    if (bitsStoredValue == "12") {
        imageFloat = imageFloat / 16.0; // 16 - 12 = 4 bits = 2^4 = 16
    } else if (bitsStoredValue == "15") {
        imageFloat = imageFloat / 2.0; // 16 - 15 = 1 bit = 2^1 = 2
    } else if (bitsStoredValue == "10") {
        imageFloat = imageFloat / 64.0; // 16 - 10 = 6 bits = 2^6 = 64
    } else if (bitsStoredValue == "14") {
        imageFloat = imageFloat / 2.0; // 16 - 14 = 2 bits = 2^2 = 4
    } else {
        // log "BITS STORED NOT EXPECTED"
    }

    imageFloat.convertTo(imageUnsigned, CV_16U, 1, -0.5); // This rounding might cause inconsistencies

    // Normalize image by dividing the intensities by the highest possible intensity so that it's dynamic range is between 0.0 and 1.0
    float highestPossibleIntensity = pow(2, atoi(bitsStoredValue.c_str())) - 1;
    imageUnsigned.convertTo(imageFloat, CV_64F);
    imageFloat = imageFloat / highestPossibleIntensity;

    // Calculate the 1st and 99th percentile
    cv::Mat imageFloatFlat = imageFloat.reshape(1, 1);
    cv::Mat imageNormSorted(imageFloatFlat.size(), CV_64F);
    cv::sort(imageFloatFlat, imageNormSorted, cv::SORT_ASCENDING);

    uint64_t nPixels = imageUnsigned.rows * imageUnsigned.cols;

    uint64_t firstIndex = 0.01 * nPixels;
    uint64_t ninenineIndex = 0.99 * nPixels;

    double firstPercentile = imageNormSorted.at<double>(firstIndex);
    double nineninePercentile = imageNormSorted.at<double>(ninenineIndex);

    // Perform the contrast stretch
    cv::Mat enhancedImage = (imageFloat - firstPercentile) / (nineninePercentile - firstPercentile) * 1.0;
    enhancedImage.setTo(0.0, imageFloat < firstPercentile);
    enhancedImage.setTo(1.0, imageFloat > nineninePercentile);

    // Calculate the median
    imageFloatFlat = enhancedImage.reshape(1, 1);
    std::vector<double> vecFromMat;
    imageFloatFlat.copyTo(vecFromMat);
    std::nth_element(vecFromMat.begin(), vecFromMat.begin() + vecFromMat.size() * 0.5, vecFromMat.end());
    double median = vecFromMat[vecFromMat.size() / 2];

    // Threshold the image at median
    enhancedImage.convertTo(imageFloat, CV_64F);
    cv::Mat imageBinarized(imageUnsigned.rows, imageUnsigned.cols, CV_64F);
    cv::threshold(imageFloat, imageBinarized, median, 1.0, cv::THRESH_BINARY);

    // Crop image
    cv::Mat points;
    cv::findNonZero(imageBinarized, points);
    cv::Rect bb = cv::boundingRect(points);

    cv::Mat imageCropped;
    if (!points.empty()) {
        imageCropped = imageFloat(bb);
    } else {
        imageCropped = imageFloat;
    }

    // Scale image
    double scalePercent = 0.5;
    unsigned newWidth = imageCropped.cols * scalePercent;
    unsigned newHeight = imageCropped.rows * scalePercent;

    cv::Mat imageDownsize(newHeight, newWidth, CV_64F);
    cv::resize(imageCropped, imageDownsize, cv::Size(newWidth, newHeight), 0.5, 0.5, cv::INTER_AREA);

    cv::Mat imageResize;
    cv::resize(imageDownsize, imageResize, cv::Size(200, 200), 0, 0, cv::INTER_AREA);

    cv::Mat horProfile(1, 200, CV_64F);
//    cv::cuda::reduce(imageResize, horProfile, 0, cv::REDUCE_AVG, CV_64F);
    cv::reduce(imageResize, horProfile, 0, cv::REDUCE_AVG, CV_64F);

    cv::Mat vertProfile(200, 1, CV_64F);
//    cv::cuda::reduce(imageResize, vertProfile, 1, cv::REDUCE_AVG, CV_64F);
    cv::reduce(imageResize, vertProfile, 1, cv::REDUCE_AVG, CV_64F);

    store(filePath, horProfile, vertProfile);

    delete dcmImage;
}

void Processor::store(std::string filePath, cv::Mat horProfile, cv::Mat vertProfile)
{
    logger->debug("Storing the calculated features into the database.");

    // Create SQL query
    std::vector<double> horVec(horProfile.begin<double>(), horProfile.end<double>());
    std::vector<double> vertVec(vertProfile.begin<double>(), vertProfile.end<double>());

    std::vector<std::string> horVecString(horVec.size());
    std::transform(horVec.begin(), horVec.end(), horVecString.begin(), [](const double& val){return std::to_string(val);});

    std::vector<std::string> vertVecString(vertVec.size());
    std::transform(vertVec.begin(), vertVec.end(), vertVecString.begin(), [](const double& val){return std::to_string(val);});

    std::string sqlQuery = "INSERT INTO " + configHandler->getTableName("features") + " (file_name, file_path, hor_profile, vert_profile) VALUES ('" +
            filePath.substr(filePath.find_last_of("/") + 1) + "', '" + filePath + "', '{" + boost::algorithm::join(horVecString, ", ") +
            "}', '{" + boost::algorithm::join(vertVecString, ", ") + "}');";

    pqxx::connection * connection = dbHandler->openConnection();

    dbHandler->executeQuery(connection, sqlQuery);

    delete connection;
}

