#ifndef UNPACKER_H
#define UNPACKER_H

#include <QObject>
#include <string>
#include <filesystem>
#include <archive.h>
#include <archive_entry.h>
#include "expectedsizes.h"
#include "confighandlers.h"

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

    std::string folderRelPath;

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
