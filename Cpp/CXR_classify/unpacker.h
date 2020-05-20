#ifndef UNPACKER_H
#define UNPACKER_H

#include <QObject>
#include <string>
#include <sys/types.h>
#include <sys/stat.h>
#include <boost/dll/runtime_symbol_info.hpp>
#include <archive.h>
#include <archive_entry.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

class Unpacker : public QObject
{
    Q_OBJECT
public:
    Unpacker(std::string url, QObject *parent = nullptr);

private:
    std::string url;
    std::string parentFolder;
    std::string filename;
    std::string filename_fullpath;
    std::string folder_name;
    std::string folder_full_path;
    std::string columns_info_name;
    std::string columns_info_full_path;

public slots:
    void unpack();

signals:
    void finished();
};

#endif // UNPACKER_H
