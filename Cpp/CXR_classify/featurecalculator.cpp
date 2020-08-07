#include "featurecalculator.h"
#include <chrono>
#include <vector>
#include <algorithm>
#include <functional>

FeatureCalculator::FeatureCalculator(ConfigHandler * configHandler, DatabaseHandler * dbHandler) : Stage(configHandler, dbHandler)
{
    FeatureCalculator::featTableName = configHandler->getTableName("features");
}

void FeatureCalculator::calculateFeatures()
{
    auto start = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed;

    emit attemptUpdateText("Calculating features");
    emit attemptUpdateProBarBounds(0, expected_num_files);

    dbHandler->addTableToDb(configHandler->getColumnsInfoPath(), "features_list", featTableName);

    emit attemptUpdateProBarValue(0);
    try
    {
        // Start a transaction
        pqxx::work w(*(dbHandler->getOutputConnection()));

        // Execute query
        pqxx::result r = w.exec("SELECT * FROM " + configHandler->getTableName("metadata") + ";");

        int count = 0;
        for (int rownum=0; rownum < r.size(); ++rownum)
        {
            // Read in the image
            const pqxx::row row = r[rownum];
            const char * filePath = row["file_path"].c_str();
            count++;

            std::cout << "Image " << count << " " << filePath << std::endl;

            DicomImage * dcmImage = new DicomImage(filePath);
            uint16_t * pixelData = (uint16_t *) (dcmImage->getOutputData(16)); // This scales the pixel values so that the intensity range is 0 - 2^16 instead of 0 - 2^bits_stored

            // Convert the image from uint16 to double
            uint64_t height = dcmImage->getHeight();
            uint64_t width = dcmImage->getWidth();

            imageUnsigned = cv::Mat(height, width, CV_16U, pixelData);
            imageUnsigned.convertTo(imageFloat, CV_64F);

            // Get the bits_stored for scaling intensities back down from 16 bits to their bits_stored value
            DcmFileFormat file_format;
            file_format.loadFile(filePath);

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

            imageFloat = preprocessing(atoi(bitsStoredValue.c_str()));

            cv::resize(imageFloat, imageResize, cv::Size(200, 200), 0, 0, cv::INTER_AREA);

            horProfile = calcHorProf();
            vertProfile = calcVertProf();

            store(filePath, horProfile, vertProfile);

            delete dcmImage;

            emit attemptUpdateProBarValue(count);
        }

        w.commit();
    }
    catch (std::exception const &e)
    {
        std::cerr << e.what() << std::endl;
    }

    emit attemptUpdateText("Done calculating features");
    emit attemptUpdateProBarValue(dbHandler->countRecords(featTableName));
    emit finished();

    auto finish = std::chrono::high_resolution_clock::now();
    elapsed = finish - start;
    std::cout << "Elapsed time: " << elapsed.count() << " s\n";
}

void FeatureCalculator::store(std::string filePath, cv::Mat horProfile, cv::Mat vertProfile)
{
    try
    {
        // Create SQL query
        std::vector<float> horVec(horProfile.begin<float>(), horProfile.end<float>());
        std::vector<float> vertVec(vertProfile.begin<float>(), vertProfile.end<float>());

        std::vector<std::string> horVecString(horVec.size());
        std::transform(horVec.begin(), horVec.end(), horVecString.begin(), [](const float& val){return std::to_string(val);});

        std::vector<std::string> vertVecString(vertVec.size());
        std::transform(vertVec.begin(), vertVec.end(), vertVecString.begin(), [](const float& val){return std::to_string(val);});

        std::string sqlQuery = "INSERT INTO " + featTableName + " (file_name, file_path, hor_profile, vert_profile) VALUES ('" +
                filePath.substr(filePath.find_last_of("/") + 1) + "', '" + filePath + "', '{" + boost::algorithm::join(horVecString, ", ") +
                "}', '{" + boost::algorithm::join(vertVecString, ", ") + "}');";

        // Start a transaction
        pqxx::work w(*(dbHandler->getInputConnection()));

        // Execute query
        pqxx::result r = w.exec(sqlQuery);

        w.commit();
    }
    catch (std::exception const &e)
    {
        std::cerr << e.what() << std::endl;
    }
}

cv::Mat FeatureCalculator::calcHorProf()
{
    cv::Mat horProfile(1, 200, CV_32F);
    cv::cuda::reduce(imageResize, horProfile, 0, cv::REDUCE_AVG, CV_32F);

    return horProfile;
}

cv::Mat FeatureCalculator::calcVertProf()
{
    cv::Mat vertProfile(200, 1, CV_32F);
    cv::cuda::reduce(imageResize, vertProfile, 1, cv::REDUCE_AVG, CV_32F);

    return vertProfile;
}

cv::Mat FeatureCalculator::preprocessing(uint8_t bitsStored)
{
    // Normalize image by dividing the intensities by the highest possible intensity so that it's dynamic range is between 0.0 and 1.0
    float highestPossibleIntensity = pow(2, bitsStored) - 1;
    imageUnsigned.convertTo(imageFloat, CV_32F);
    imageFloat = imageFloat / highestPossibleIntensity;

    // Calculate the 1st and 99th percentile
    imageFloatFlat = imageFloat.reshape(1, 1);
    cv::Mat imageNormSorted(imageFloatFlat.size(), CV_32F);
    cv::sort(imageFloatFlat, imageNormSorted, cv::SORT_ASCENDING);

    uint64_t nPixels = imageUnsigned.rows * imageUnsigned.cols;

    uint64_t firstIndex = 0.01 * nPixels;
    uint64_t ninenineIndex = 0.99 * nPixels;

    float firstPercentile = imageNormSorted.at<float>(firstIndex);
    float nineninePercentile = imageNormSorted.at<float>(ninenineIndex);

    // Perform the contrast stretch
    cv::Mat enhancedImage = (imageFloat - firstPercentile) / (nineninePercentile - firstPercentile) * 1.0;
    enhancedImage.setTo(0.0, imageFloat < firstPercentile);
    enhancedImage.setTo(1.0, imageFloat > nineninePercentile);

    // Calculate the median
    imageFloatFlat = enhancedImage.reshape(1, 1);
    std::vector<float> vecFromMat;
    imageFloatFlat.copyTo(vecFromMat);
    std::nth_element(vecFromMat.begin(), vecFromMat.begin() + vecFromMat.size() * 0.5, vecFromMat.end());
    float median = vecFromMat[vecFromMat.size() / 2];

    // Threshold the image at median
    enhancedImage.convertTo(imageFloat, CV_32F);
    cv::Mat imageBinarized(imageUnsigned.rows, imageUnsigned.cols, CV_32F);
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
    float scalePercent = 0.5;
    unsigned width = imageCropped.cols * scalePercent;
    unsigned height = imageCropped.rows * scalePercent;

    cv::Mat imageDownsize(height, width, CV_32F);

    cv::resize(imageCropped, imageDownsize, cv::Size(width, height), 0.5, 0.5, cv::INTER_AREA);

    return imageDownsize;
}



