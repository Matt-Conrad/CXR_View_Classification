#ifndef UNPACKER_H
#define UNPACKER_H

#include <QObject>
#include <string>
#include <archive.h>
#include <archive_entry.h>

class Unpacker : public QObject
{
    Q_OBJECT
public:
    Unpacker(std::string filename_fullpath, QObject *parent = nullptr);

private:
    std::string filename_fullpath;

public slots:
    void unpack();

signals:
    void finished();
};

#endif // UNPACKER_H
