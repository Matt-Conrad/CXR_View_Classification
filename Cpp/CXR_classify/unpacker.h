#ifndef UNPACKER_H
#define UNPACKER_H

#include <QObject>
#include <string>
#include <filesystem>
#include <archive.h>
#include <archive_entry.h>
#include "confighandler.h"
#include "stage.h"

class Unpacker : public Stage
{
    Q_OBJECT

friend class AppController;

public:
    Unpacker(ConfigHandler *);

private:
    int extract(const char *, std::string);
    int copy_data(struct archive *ar, struct archive *aw);

    std::string folderRelPath;

    quint64 countDcms();

public slots:
    void unpack();
};

#endif // UNPACKER_H
