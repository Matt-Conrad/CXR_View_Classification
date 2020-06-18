#ifndef UNPACKER_H
#define UNPACKER_H

#include <QObject>
#include <string>
#include <filesystem>
#include <archive.h>
#include <archive_entry.h>

class Unpacker : public QObject
{
    Q_OBJECT
public:
    Unpacker(std::string, std::string, std::string, std::string);

private:
    std::string filename_fullpath;
    std::string folder_full_path;
    std::string parentFolder;
    std::string dataset;

public slots:
    void unpack();

signals:
    void finished();
};

#endif // UNPACKER_H
