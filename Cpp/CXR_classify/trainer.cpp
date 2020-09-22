#include "trainer.h"

Trainer::Trainer(ConfigHandler * configHandler, DatabaseHandler * dbHandler) : Runnable(configHandler, dbHandler)
{

}

void Trainer::run()
{
    emit attemptUpdateText("Training classifier");
    emit attemptUpdateProBarBounds(0, expected_num_files);
    emit attemptUpdateProBarValue(0);

    std::string sqlQuery = "SELECT file_name, hor_profile, vert_profile FROM " + configHandler->getTableName("features") + " ORDER BY file_path ASC;";

    pqxx::result profileResults = dbHandler->executeQuery(dbHandler->connection, sqlQuery);

    std::vector<std::string> fileNames = {};
    static double X[numSamples][400];

    // Put all labels into a list
    sqlQuery = "SELECT image_view FROM " + configHandler->getTableName("label") + " ORDER BY file_path ASC;";
    // Execute query
    std::vector<size_t> y = {};
    pqxx::result labelsResult = dbHandler->executeQuery(dbHandler->connection, sqlQuery);

    for (int rownum = 0; rownum < profileResults.size(); rownum++) {
        // Filenames
        std::string filename(profileResults[rownum]["file_name"].c_str());
        fileNames.push_back(filename);

        // Horizontal profile
        pqxx::array_parser hor_parser = profileResults[rownum]["hor_profile"].as_array();
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
        pqxx::array_parser vert_parser = profileResults[rownum]["vert_profile"].as_array();
        currentObject = vert_parser.get_next();
        featureIndex = 200;
        while (currentObject.first != pqxx::array_parser::juncture::done) {
            if (currentObject.second != "") {
                X[rownum][featureIndex] = std::stod(currentObject.second);
                featureIndex++;
            }
            currentObject = vert_parser.get_next();
        }

        // Filenames
        std::string label(labelsResult[rownum]["image_view"].c_str());
        if (label == "F") {
            y.push_back(0);
        } else if (label == "L") {
            y.push_back(1);
        }
    }

    // First, load the data.
    arma::mat xArma(&X[0][0], 400, numSamples); // transpose because Armadillo stores data column-by-column (for compatibility with LAPACK)
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

    emit attemptUpdateText(result.c_str());
    emit attemptUpdateProBarValue(expected_num_files);

    emit finished();
}
