#ifndef UNPACKER_H
#define UNPACKER_H

#include <string>
#include <archive.h>
#include <archive_entry.h>

class Unpacker{
    public:
        Unpacker(const char *, const char *);
        void run();

        std::string fileRelPathStr;
        std::string folderRelPathStr;

    private: 
        int extract(const char *, std::string);
        int copy_data(struct archive *, struct archive *);
};

// These functions can be called from "C" 
extern "C" {
    Unpacker * Unpacker_new(const char *, const char *);
    void Unpacker_run(Unpacker *);
}

#endif // UNPACKER_H