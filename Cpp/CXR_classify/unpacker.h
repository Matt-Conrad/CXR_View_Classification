#ifndef UNPACKER_H
#define UNPACKER_H

#include <QObject>
#include <string>
#include <filesystem>
#include <archive.h>
#include <archive_entry.h>
#include <unordered_map>
#include <fstream>
#include <iostream>
#include <boost/iostreams/filtering_streambuf.hpp>
#include <boost/iostreams/copy.hpp>
#include <boost/iostreams/filter/gzip.hpp>
#include "confighandlers.h"

const std::unordered_map<std::string, uint16_t> expected_num_files_in_dataset = {
        {"NLMCXR_subset_dataset.tgz", 10},
        {"NLMCXR_dcm.tgz", 7470}
    };

class Unpacker : public QObject
{
    Q_OBJECT

friend class AppController;

public:
    Unpacker(ConfigHandler *);

private:
    ConfigHandler * configHandler;

    int extract(const char *, std::string);
    int copy_data(struct archive *ar, struct archive *aw);

    quint64 expected_num_files;

    quint64 countDcms();

public slots:
    void unpack();

signals:
    void finished();
    void attemptUpdateProBarValue(quint64);
    void attemptUpdateProBarBounds(quint64, quint64);
    void attemptUpdateText(QString);
};

#endif // UNPACKER_H
