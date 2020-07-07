#include "labeler.h"

Labeler::Labeler(std::string configFilename, std::string columnsInfo) : QWidget()
{
    Labeler::configFilename = configFilename;
    Labeler::columnsInfo = columnsInfo;
    Labeler::labelTableName = config::getSection(configFilename, "table_info").get<std::string>("label_table_name");

    Labeler::dbInfo = config::getSection(configFilename, "postgresql");
}

void Labeler::closeLabelApp()
{
    closeConnection();
    emit attemptUpdateText("Image labeling complete");
    emit finished();
    this->close();
}

void Labeler::closeConnection()
{
    bdo::deleteConnection(connection);
}

void Labeler::fillWindow()
{
    queryImageList();
    emit attemptUpdateText("Please manually label images");
    bdo::addTableToDb(dbInfo, columnsInfo, "labels", labelTableName);
    QGridLayout * layout = new QGridLayout;
    layout->addWidget(label, 0, 0, 1, 2);
    layout->addWidget(image, 1, 0, 1, 2);
    layout->addWidget(frontalButton, 2, 0);
    layout->addWidget(lateralButton, 2, 1);

    // Set layout
    this->setLayout(layout);
    displayNextImage();
    connect(this->frontalButton, SIGNAL(clicked()), this, SLOT(frontal()));
    connect(this->lateralButton, SIGNAL(clicked()), this, SLOT(lateral()));
    this->show();
}

void Labeler::frontal()
{
    label->setText("Frontal");
    storeLabel("F");
    displayNextImage();
}

void Labeler::lateral()
{
    label->setText("Lateral");
    storeLabel("L");
    displayNextImage();
}

void Labeler::displayNextImage()
{
    if (record == imageList.end()) {
        emit attemptUpdateText("Done labeling");
        closeLabelApp();
    } else {
        count++;
        this->setWindowTitle("Image Count "  + QString::number(count));
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
        image->setPixmap(pixmap);
    }
}

void Labeler::storeLabel(std::string decision)
{
    std::string labelTableName = config::getSection(configFilename, "table_info").get<std::string>("label_table_name");
    std::string filePath = record["file_path"].c_str();
    std::string fileName = filePath.substr(filePath.find_last_of("/") + 1);
    std::string sqlQuery = "INSERT INTO " + labelTableName + "  (file_name, file_path, image_view) VALUES ('" + fileName + "', '" +
            filePath + "', '" + decision + "');";
    std::cout << sqlQuery << std::endl;

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
    std::string metadataTableName = config::getSection(configFilename, "table_info").get<std::string>("metadata_table_name");
    std::string sqlQuery = "SELECT file_path, bits_stored FROM " + metadataTableName + " ORDER BY file_path;";
    try
    {
        // Connect to the database
        connection = bdo::openConnection(dbInfo);

        // Start a transaction
        pqxx::work imageListTransaction(*connection);

        // Execute query
        imageList = imageListTransaction.exec(sqlQuery);
        record = imageList.begin();

        imageListTransaction.commit();
    }
    catch (std::exception const &e)
    {
        std::cout << "error" << std::endl;
    }
}


