#ifndef UNPACKER_H
#define UNPACKER_H

#include <string>
#include <archive.h>
#include <archive_entry.h>
#include "confighandler.h"

class Unpacker {
    public:
        Unpacker();
        void run();

    private: 
        ConfigHandler * configHandler = new ConfigHandler("config.ini");

        int extract(const char *, std::string);
        int copy_data(struct archive *, struct archive *);
};

// These functions can be called from "C" 
extern "C" {
    Unpacker * Unpacker_new();
    void Unpacker_run(Unpacker *);
}

#endif // UNPACKER_H