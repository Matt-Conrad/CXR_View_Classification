#ifndef UNPACKER_H
#define UNPACKER_H

#include <QObject>
#include <string>
#include <filesystem>
#include <archive.h>
#include <archive_entry.h>
#include "confighandler.h"
#include "runnable.h"

class Unpacker : public Runnable
{
public:
    Unpacker(ConfigHandler *);

private:
    int extract(const char *, std::string);
    int copy_data(struct archive *ar, struct archive *aw);

    std::string folderRelPath;

    quint64 countDcms();

public slots:
    void run();
};

#endif // UNPACKER_H
