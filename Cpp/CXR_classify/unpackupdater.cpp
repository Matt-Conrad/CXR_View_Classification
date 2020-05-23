#include "unpackupdater.h"

UnpackUpdater::UnpackUpdater(std::string folder_full_path, std::string dataset) : QObject()
{
    UnpackUpdater::folder_full_path = folder_full_path;
    UnpackUpdater::dataset = dataset;
}

void UnpackUpdater::updateProgressBar()
{
    emit attemptUpdateText("Unpacking images");
    emit attemptUpdateProBarBounds(0, expected_num_files);

    while (!std::filesystem::is_directory(folder_full_path)) {
        ;
    }

    emit attemptUpdateProBarValue(0);
    while (countDcms() < expected_num_files) {
        emit attemptUpdateProBarValue(countDcms());
    }
    emit attemptUpdateProBarValue(countDcms());
    emit attemptUpdateText("Images unpacked");

    emit finished();
}

quint64 UnpackUpdater::countDcms()
{
    quint64 count = 0;
    for (auto & p : std::filesystem::recursive_directory_iterator(folder_full_path)) {
        if (p.path().extension() == ".dcm") {
            count++;
        }
    }
    return count;
}


