#include "trainer.h"

Trainer::Trainer(std::string dbConfigFilename, std::string featTableName, std::string labelTableName, std::string filename) : QObject()
{
    Trainer::featTableName = featTableName;
    Trainer::labelTableName = labelTableName;

    Trainer::host = config::getSection(dbConfigFilename, "postgresql").get<std::string>("host");
    Trainer::port = config::getSection(dbConfigFilename, "postgresql").get<std::string>("port");
    Trainer::database = config::getSection(dbConfigFilename, "postgresql").get<std::string>("database");
    Trainer::user = config::getSection(dbConfigFilename, "postgresql").get<std::string>("user");
    Trainer::password = config::getSection(dbConfigFilename, "postgresql").get<std::string>("password");

    Trainer::expected_num_files = expected_num_files_in_dataset.at(filename);
}

void Trainer::trainClassifier()
{
    emit attemptUpdateText("Training classifier");
    try
    {
        // Connect to the database
        pqxx::connection c("host=" + host + " port=" + port + " dbname=" + database + " user=" + user + " password=" + password);

        // Start a transaction
        pqxx::work w(c);

        std::string sqlQuery = "SELECT file_name, hor_profile, vert_profile FROM " + featTableName + " ORDER BY file_path ASC;";

        // Execute query
        pqxx::result r = w.exec(sqlQuery);

        std::vector<std::string> fileNames = {};
        static double X[10][400];

        for (int rownum = 0; rownum < r.size(); rownum++) {
            // Filenames
            std::string filename(r[rownum]["file_name"].c_str());
            fileNames.push_back(filename);

            // Horizontal profile
            pqxx::array_parser hor_parser = r[rownum]["hor_profile"].as_array();
            std::pair<pqxx::array_parser::juncture, std::string>  currentObject = hor_parser.get_next();
            int featureIndex = 0;
            while (currentObject.first != pqxx::array_parser::juncture::done) {
                if (currentObject.second != "") {
                    X[rownum][featureIndex] = std::stod(currentObject.second);
                    featureIndex++;
                }
                currentObject = hor_parser.get_next();
            }

            // Vertical profile
            pqxx::array_parser vert_parser = r[rownum]["vert_profile"].as_array();
            currentObject = vert_parser.get_next();
            featureIndex = 200;
            while (currentObject.first != pqxx::array_parser::juncture::done) {
                if (currentObject.second != "") {
                    X[rownum][featureIndex] = std::stod(currentObject.second);
                    featureIndex++;
                }
                currentObject = vert_parser.get_next();
            }
        }

        // Put all labels into a list
        sqlQuery = "SELECT image_view FROM " + labelTableName + " ORDER BY file_path ASC;";
        // Execute query
        std::vector<size_t> y = {};
        pqxx::result labelsResult = w.exec(sqlQuery);
        for (int rownum = 0; rownum < r.size(); rownum++) {
            // Filenames
            std::string label(labelsResult[rownum]["image_view"].c_str());
            if (label == "F") {
                y.push_back(0);
            } else if (label == "L") {
                y.push_back(1);
            }
        }

        // First, load the data.
        arma::mat xArma(&X[0][0], 400, 10); // transpose because Armadillo stores data column-by-column (for compatibility with LAPACK)
        arma::Row yArma(y);
        arma::mat xTrain, xTest;
        arma::Row<size_t> yTrain, yTest;

        mlpack::data::Split(xArma, yArma, xTrain, xTest, yTrain, yTest, 0.33, true);

        const size_t numClasses = 2;

        int nSplits = 10;
        double cvAcc;
        if (xTrain.n_cols < nSplits) {
            mlpack::cv::KFoldCV<mlpack::svm::LinearSVM<>, mlpack::cv::Accuracy> cv(xTrain.n_cols, xTrain, yTrain, numClasses);
            cvAcc = cv.Evaluate();
        } else {
            mlpack::cv::KFoldCV<mlpack::svm::LinearSVM<>, mlpack::cv::Accuracy> cv(nSplits, xTrain, yTrain, numClasses);
            cvAcc = cv.Evaluate();
        }

        std::string result("KFoldCV Accuracy: " + std::to_string(cvAcc));
        emit attemptUpdateText(result.c_str());

    }
    catch (std::exception const &e)
    {
        std::cout << e.what() << std::endl;
    }
    emit finished();
}
