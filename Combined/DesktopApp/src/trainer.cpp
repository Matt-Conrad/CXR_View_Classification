#include "trainer.h"

Trainer::Trainer()
{

}

void Trainer::run()
{
    std::string sqlQuery = "SELECT file_name, hor_profile, vert_profile FROM " + configHandler->getTableName("features") + " ORDER BY file_path ASC;";

    pqxx::result profileResults = dbHandler->executeQuery(dbHandler->connection, sqlQuery);

    std::vector<std::string> fileNames = {};

    // Put all labels into a list
    sqlQuery = "SELECT image_view FROM " + configHandler->getTableName("label") + " ORDER BY file_path ASC;";
    // Execute query
    std::vector<size_t> y = {};
    pqxx::result labelsResult = dbHandler->executeQuery(dbHandler->connection, sqlQuery);

    int expectedNumFiles = expected_num_files_in_dataset.at(configHandler->getDatasetType());
    arma::mat xArma(400, expectedNumFiles, arma::fill::zeros); // transpose because Armadillo stores data column-by-column (for compatibility with LAPACK)

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
                xArma(featureIndex, rownum) = std::stod(currentObject.second);
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
                xArma(featureIndex, rownum) = std::stod(currentObject.second);
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

    arma::Row yArma(y);
    arma::mat xTrain, xTest;
    arma::Row<size_t> yTrain, yTest;

    mlpack::data::Split(xArma, yArma, xTrain, xTest, yTrain, yTest, 0.33);

    const size_t numClasses = 2;
    int nSplits = 10;
    int numSamplesInTrain = xTrain.n_cols;
    double cvAcc;
    if (numSamplesInTrain < nSplits) {
        mlpack::cv::KFoldCV<mlpack::svm::LinearSVM<>, mlpack::cv::Accuracy> cv(xTrain.n_cols, xTrain, yTrain, numClasses);
        cvAcc = cv.Evaluate();
    } else {
        std::vector<double> results;
        for (int i = 0; i < 10; i++) {
            TrainProcessor * trainProcessor = new TrainProcessor(xTrain, yTrain, i, &results, configHandler, dbHandler);
            threadpool->start(trainProcessor);
        }
        threadpool->waitForDone();
        cvAcc = accumulate(results.begin(), results.end(), 0.0) / results.size();
    }

    std::string result("KFoldCV Accuracy: " + std::to_string(cvAcc));
    std::cout << result << std::endl;
}

Trainer * Trainer_new() { 
    return new Trainer(); 
}

void Trainer_run(Trainer * trainer) {
    trainer->run();
}


TrainProcessor::TrainProcessor(arma::mat xTrain, arma::Row<size_t> yTrain, int index, std::vector<double> * results, ConfigHandler * configHandler, DatabaseHandler * dbHandler)
{
    TrainProcessor::configHandler = configHandler;
    TrainProcessor::dbHandler = dbHandler;
    TrainProcessor::xTrain = xTrain;
    TrainProcessor::yTrain = yTrain;
    TrainProcessor::index = index;
    TrainProcessor::results = results;
}

void TrainProcessor::run()
{
    double subsetIncrements = ((double) xTrain.n_cols) / 10;
    int firstIndex = std::round(index * subsetIncrements); // may need to subtract 1
    int secondIndex = std::round((index+1) * subsetIncrements) - 1;

    mlpack::svm::LinearSVM<> lsvm(xTrain.cols(firstIndex, secondIndex), yTrain.cols(firstIndex, secondIndex));
    arma::Row<size_t> predictedLabels;

    xTrain.shed_cols(firstIndex, secondIndex);
    yTrain.shed_cols(firstIndex, secondIndex);

    lsvm.Classify(xTrain, predictedLabels);
    size_t numberOfCorrectPredictions = arma::sum(predictedLabels == yTrain);
    double accuracy = ((double) numberOfCorrectPredictions) / yTrain.n_elem;
    results->push_back(accuracy);
}