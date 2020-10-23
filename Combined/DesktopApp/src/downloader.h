#ifndef DOWNLOADER_H
#define DOWNLOADER_H

#include <string>
#include <filesystem>
#include <QtNetwork>
#include "confighandler.h"

class Downloader {
    public:
        Downloader();
        void run();

    private:
        std::string filenameAbsPath;
        uint64_t expected_size;

        ConfigHandler * configHandler = new ConfigHandler("config.ini");

        int download();
};

// These functions can be called from "C"
extern "C" {
    Downloader * Downloader_new();
    void Downloader_run(Downloader *);
}

#endif // DOWNLOADER_H
