#include "labeler.h"

Labeler::Labeler(ConfigHandler * configHandler, DatabaseHandler * dbHandler) : Runnable(configHandler, dbHandler)
{
    Labeler::labelTableName = configHandler->getTableName("label");
}

void Labeler::run()
{
    queryImageList();
    emit attemptUpdateText("Please manually label images");
    emit attemptUpdateProBarBounds(0, expected_num_files);

    dbHandler->addTableToDb(configHandler->getColumnsInfoPath(), "labels", labelTableName);

    displayNextImage();

    while (count < expected_num_files) {
        ;
    }

    emit attemptUpdateText("Image labeling complete");
    emit finished();
}

void Labeler::frontal()
{
    storeLabel("F");
    count++;
    displayNextImage();
}

void Labeler::lateral()
{
    storeLabel("L");
    count++;
    displayNextImage();
}

void Labeler::displayNextImage()
{
    emit attemptUpdateText("Image count: " + QString::number(count));
    emit attemptUpdateProBarValue(count);

    if (count < expected_num_files) {
        const char * filePath = record["file_path"].c_str();
        DicomImage * dcmImage = new DicomImage(filePath);
        uchar * pixelData = (uchar *) (dcmImage->getOutputData(8));

        int height = dcmImage->getHeight();
        int width = dcmImage->getWidth();

        cv::Mat originalImage(height, width, CV_8U, pixelData);
        cv::Mat imageSquare(height, width, CV_8U);
        cv::resize(originalImage, imageSquare, cv::Size(300, 300), 0, 0, cv::INTER_AREA);

        QImage qImage(imageSquare.data, 300, 300, QImage::Format_Grayscale8);
        QPixmap pixmap = QPixmap::fromImage(qImage);

        emit attemptUpdateImage(pixmap);
    }
}

void Labeler::storeLabel(std::string decision)
{
    std::string filePath = record["file_path"].c_str();
    std::string fileName = filePath.substr(filePath.find_last_of("/") + 1);
    std::string sqlQuery = "INSERT INTO " + labelTableName + "  (file_name, file_path, image_view) VALUES ('" + fileName + "', '" +
            filePath + "', '" + decision + "');";
    try
    {
        // Start a transaction
        pqxx::work storeTransaction(*connection);
        storeTransaction.exec(sqlQuery);
        storeTransaction.commit();
    }
    catch (std::exception const &e)
    {
        std::cerr << e.what() << std::endl;
    }

    record++;
}

void Labeler::queryImageList()
{
    std::string sqlQuery = "SELECT file_path, bits_stored FROM " + configHandler->getTableName("metadata") + " ORDER BY file_path;";
    try
    {
        // Connect to the database
        connection = dbHandler->openConnection();

        // Start a transaction
        pqxx::work imageListTransaction(*connection);

        // Execute query
        imageList = imageListTransaction.exec(sqlQuery);
        record = imageList.begin();

        imageListTransaction.commit();
    }
    catch (std::exception const &e)
    {
        // log "error"
    }
}


