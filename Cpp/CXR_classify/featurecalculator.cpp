#include "featurecalculator.h"

FeatureCalculator::FeatureCalculator(ConfigHandler * configHandler, DatabaseHandler * dbHandler) : QObject()
{
    FeatureCalculator::configHandler = configHandler;
    FeatureCalculator::dbHandler = dbHandler;

    FeatureCalculator::featTableName = configHandler->getTableName("features");
    FeatureCalculator::expected_num_files = expected_num_files_in_dataset.at(configHandler->getTgzFilename());
}

void FeatureCalculator::calculateFeatures()
{
    emit attemptUpdateText("Calculating features");
    emit attemptUpdateProBarBounds(0, expected_num_files);

    dbHandler->addTableToDb(configHandler->getColumnsInfoPath(), "features_list", featTableName);

    emit attemptUpdateProBarValue(0);
    try
    {
        // Connect to the database
        pqxx::connection * connection = dbHandler->openConnection();

        // Start a transaction
        pqxx::work w(*connection);

        // Execute query
        pqxx::result r = w.exec("SELECT * FROM " + configHandler->getTableName("metadata") + ";");

        quint64 count = 0;
        for (int rownum=0; rownum < r.size(); ++rownum)
        {
            const pqxx::row row = r[rownum];
            const char * filePath = row["file_path"].c_str();
            count++;

            DicomImage * dcmImage = new DicomImage(filePath);
            uint16_t * pixelData = (uint16_t *) (dcmImage->getOutputData(16)); // This scales the pixel values so that the intensity range is 0 - 2^16 instead of 0 - 2^bits_stored

            uint64_t height = dcmImage->getHeight();
            uint64_t width = dcmImage->getWidth();

            // Need to divide this by 16 for some reason. Probably because the bits stored is 12 but the values that are read are scaled to 16 bits?
            cv::Mat originalImage(height, width, CV_16U, pixelData);
            cv::Mat originalImageDouble;
            originalImage.convertTo(originalImageDouble, CV_64F);

            //DEBUGGING
            DcmFileFormat file_format;
            file_format.loadFile(filePath);

            DcmTagKey bitsStoredKey(40, 257); // bits stored
            OFString bitsStoredValue;
            file_format.getDataset()->findAndGetOFString(bitsStoredKey, bitsStoredValue);

            cv::Mat rawIntensityImage(originalImage.rows, originalImage.cols, CV_64F);
            // We must scale the intensities back down from 16 bits to either 12 or 15
            if (bitsStoredValue == "12") {
                rawIntensityImage = originalImageDouble / 16.0; // 16 - 12 = 4 bits = 2^4 = 16
            } else if (bitsStoredValue == "15") {
                rawIntensityImage = originalImageDouble / 2.0; // 16 - 15 = 1 bit = 2^1 = 2
            } else if (bitsStoredValue == "10") {
                rawIntensityImage = originalImageDouble / 64.0; // 16 - 10 = 6 bits = 2^6 = 64
            } else if (bitsStoredValue == "14") {
                rawIntensityImage = originalImageDouble / 2.0; // 16 - 14 = 2 bits = 2^2 = 4
            } else {
                std::cout << "BITS STORED NOT EXPECTED" << std::endl;
            }

            cv::Mat rawIntensityImageInt;
            rawIntensityImage.convertTo(rawIntensityImageInt, CV_16U);//, 1, -0.5); // This rounding might cause inconsistencies

//            std::ofstream myfile;
//            myfile.open("./cpp.csv");
//            myfile<< cv::format(rawIntensityImageInt, cv::Formatter::FMT_CSV) << std::endl;
//            myfile.close();
//            std::cout << "Image saved" << std::endl;
//            std::this_thread::sleep_for(std::chrono::seconds(100));

            DcmTagKey photometricKey(40, 4); // photometric interpretation
            OFString photometricValue;
            file_format.getDataset()->findAndGetOFString(photometricKey, photometricValue);

            std::cout << filePath << std::endl;

            cv::Mat preprocessedImage = preprocessing(rawIntensityImage, photometricValue.c_str(), atoi(bitsStoredValue.c_str()));

//            std::cout << "Preprocessed" << std::endl;

            cv::Mat horProfile = calcHorProf(preprocessedImage, 200, 200);
//            std::cout << "Horizontal Profile" << std::endl;
            cv::Mat vertProfile = calcVertProf(preprocessedImage, 200, 200);
//            std::cout << "Vertical Profile" << std::endl;

            store(filePath, horProfile, vertProfile);

//            std::cout << "Stored" << std::endl;

            delete dcmImage;

            emit attemptUpdateProBarValue(count);
        }

        w.commit();
        dbHandler->deleteConnection(connection);
    }
    catch (std::exception const &e)
    {
        std::cerr << e.what() << std::endl;
    }
    emit attemptUpdateText("Done calculating features");
    emit attemptUpdateProBarValue(dbHandler->countRecords(featTableName));

    emit finished();
}

void FeatureCalculator::store(std::string filePath, cv::Mat horProfile, cv::Mat vertProfile)
{
    try
    {
        // Connect to the database
        pqxx::connection * connection = dbHandler->openConnection();

        // Create SQL query
        std::vector<float> horVec(horProfile.begin<float>(), horProfile.end<float>());
        std::vector<float> vertVec(vertProfile.begin<float>(), vertProfile.end<float>());

        std::vector<std::string> horVecString(horVec.size());
        std::transform(horVec.begin(), horVec.end(), horVecString.begin(), [](const float& val)
        {
            return std::to_string(val);
        });

//        std::cout << "Hor profile: " << horProfile << std::endl;
//        std::this_thread::sleep_for(std::chrono::seconds(100));

        std::vector<std::string> vertVecString(vertVec.size());
        std::transform(vertVec.begin(), vertVec.end(), vertVecString.begin(), [](const float& val)
        {
            return std::to_string(val);
        });

//        std::cout << "Vert profile: " << vertProfile << std::endl;
//        std::this_thread::sleep_for(std::chrono::seconds(100));

        std::string sqlQuery = "INSERT INTO " + featTableName + " (file_name, file_path, hor_profile, vert_profile) VALUES ('" +
                filePath.substr(filePath.find_last_of("/") + 1) + "', '" + filePath + "', '{" + boost::algorithm::join(horVecString, ", ") +
                "}', '{" + boost::algorithm::join(vertVecString, ", ") + "}');";

//        std::cout << sqlQuery << std::endl;
//        std::this_thread::sleep_for(std::chrono::seconds(100));

        // Start a transaction
        pqxx::work w(*connection);

        // Execute query
        pqxx::result r = w.exec(sqlQuery);

        w.commit();
        dbHandler->deleteConnection(connection);
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

    cv::Mat horProfile(1, width, CV_32F);
    cv::reduce(imageSquare, horProfile, 0, cv::REDUCE_AVG, CV_32F);

//    std::ofstream myfile;
//    myfile.open("./cpp.csv");
//    myfile<< cv::format(horProfile, cv::Formatter::FMT_CSV) << std::endl;
//    myfile.close();
//    std::cout << "Image saved" << std::endl;
//    std::this_thread::sleep_for(std::chrono::seconds(100));

    return horProfile;
}

cv::Mat FeatureCalculator::calcVertProf(cv::Mat image, unsigned width, unsigned height)
{
    cv::Mat imageSquare(height, width, CV_32F);
    cv::resize(image, imageSquare, cv::Size(width, height), 0, 0, cv::INTER_AREA);

    cv::Mat vertProfile(height, 1, CV_32F);
    cv::reduce(imageSquare, vertProfile, 1, cv::REDUCE_AVG, CV_32F);

//    std::ofstream myfile;
//    myfile.open("./cpp2.csv");
//    myfile<< cv::format(vertProfile, cv::Formatter::FMT_CSV) << std::endl;
//    myfile.close();
//    std::cout << "Image saved" << std::endl;
//    std::this_thread::sleep_for(std::chrono::seconds(100));

    return vertProfile;
}

cv::Mat FeatureCalculator::preprocessing(cv::Mat image, std::string photometric, uint8_t bitsStored)
{
//    std::cout << image.type() << std::endl;
//    std::vector<int> compression_params;
//    compression_params.push_back(cv::IMWRITE_PNG_COMPRESSION);
//    compression_params.push_back(0);
//    cv::imwrite("./image.png", image, compression_params);
//    std::this_thread::sleep_for(std::chrono::seconds(100));

    // Normalize image by dividing the intensities by the highest possible intensity so that it's dynamic range is between 1.0
    double highestPossibleIntensity = pow(2, bitsStored) - 1;
    cv::Mat imageDouble(image.rows, image.cols, CV_64F);
    image.convertTo(imageDouble, CV_64F);
    cv::Mat imageNorm(image.rows, image.cols, CV_64F);
    imageNorm = imageDouble / highestPossibleIntensity;

//    std::cout << "Normalized" << std::endl;

    // Invert the image if it's monochrome 1
//    if (photometric == "MONOCHROME1") {
//        imageNorm = 1.0 - imageNorm;
//    }

//    std::ofstream myfile;
//    myfile.open("./cpp2.csv");
//    myfile<< cv::format(imageNorm, cv::Formatter::FMT_CSV) << std::endl;
//    myfile.close();
//    std::cout << "Image saved" << std::endl;
//    std::this_thread::sleep_for(std::chrono::seconds(100));

//    std::cout << "Inverted" << std::endl;

    cv::Mat imageNormFlat = imageNorm.reshape(1, 1);
    cv::Mat imageNormSorted;
    cv::sort(imageNormFlat, imageNormSorted, cv::SORT_ASCENDING);

    uint64_t nPixels = image.rows * image.cols;

    uint64_t firstIndex = 0.01 * nPixels;
    uint64_t ninenineIndex = 0.99 * nPixels;

    double firstPercentile = imageNormSorted.at<double>(firstIndex);
    double nineninePercentile = imageNormSorted.at<double>(ninenineIndex);

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

//    std::cout << "Enhanced" << std::endl;

    cv::Mat enhancedImageFloat(image.rows, image.cols, CV_32F);
    enhancedImage.convertTo(enhancedImageFloat, CV_32F);

    cv::Mat enhancedImageFlat = enhancedImageFloat.reshape(1, 1);
    cv::Mat enhancedImageSorted;
    cv::sort(enhancedImageFlat, enhancedImageSorted, cv::SORT_ASCENDING);

    uint64_t medianIndex = 0.50 * nPixels;
    float median = enhancedImageSorted.at<float>(medianIndex);

    cv::Mat imageBinarized(image.rows, image.cols, CV_32F);
    cv::threshold(enhancedImageFloat, imageBinarized, median, 1.0, cv::THRESH_BINARY);

//    std::cout << "Binarized" << std::endl;

//    std::cout << "1st percentile: " << firstPercentile << std::endl;
//    std::cout << "Median: " << median << std::endl;
//    std::cout << "99th percentile: " << nineninePercentile << std::endl;

    cv::Mat points;
    cv::findNonZero(imageBinarized, points);
    cv::Rect bb = cv::boundingRect(points);

//    std::cout << "Bounding" << std::endl;

    cv::Mat imageCropped = enhancedImageFloat(bb);

//    std::cout << "Cropped" << std::endl;

    float scalePercent = 0.5;
    unsigned width = imageCropped.cols * scalePercent;
    unsigned height = imageCropped.rows * scalePercent;

    cv::Mat imageDownsize(height, width, CV_32F);

    cv::resize(imageCropped, imageDownsize, cv::Size(width, height), 0.5, 0.5, cv::INTER_AREA);

//    std::cout << "Downsized" << std::endl;

//    cv::namedWindow("image", cv::WINDOW_NORMAL);
//    cv::imshow("image", imageDownsize);
//    cv::waitKey(0);

    return imageDownsize;
}



