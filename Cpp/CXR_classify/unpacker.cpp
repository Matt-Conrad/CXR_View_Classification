#include "unpacker.h"

#include <chrono>
#include <iostream>

Unpacker::Unpacker(ConfigHandler * configHandler) : Runnable(configHandler)
{
    folderAbsPath = configHandler->getUnpackFolderPath();
}

int Unpacker::copy_data(struct archive * ar, struct archive * aw)
{
    int r;
    const void *buff;
    size_t size;
    off_t offset;

    for (;;) {
        r = archive_read_data_block(ar, &buff, &size, &offset);
        if (r == ARCHIVE_EOF)
            return (ARCHIVE_OK);
        if (r < ARCHIVE_OK)
            return (r);
        r = archive_write_data_block(aw, buff, size, offset);
        if (r < ARCHIVE_OK) {
            fprintf(stderr, "%s\n", archive_error_string(aw));
            return (r);
        }
    }
}

int Unpacker::extract(const char * filename, std::string destination)
{
    struct archive *a;
    struct archive *ext;
    struct archive_entry *entry;
    int flags;
    int r;

    /* Select which attributes we want to restore. */
    flags = ARCHIVE_EXTRACT_TIME;
    flags |= ARCHIVE_EXTRACT_PERM;
    flags |= ARCHIVE_EXTRACT_ACL;
    flags |= ARCHIVE_EXTRACT_FFLAGS;

    a = archive_read_new();
    archive_read_support_format_all(a);
    archive_read_support_compression_all(a);
    ext = archive_write_disk_new();
    archive_write_disk_set_options(ext, flags);
    archive_write_disk_set_standard_lookup(ext);
    if ((r = archive_read_open_filename(a, filename, 10240))) // read in TGZ
        return 1;

    for (;;) {
        r = archive_read_next_header(a, &entry); // get next file to unpack in TGZ
        if (r == ARCHIVE_EOF)
            break;
        if (r < ARCHIVE_OK)
            fprintf(stderr, "%s\n", archive_error_string(a));
        if (r < ARCHIVE_WARN)
            return 1;
        // This is for the full set
        const char* currentFile = archive_entry_pathname(entry);
        const std::string fullOutputPath = destination + "/" + currentFile;
        archive_entry_set_pathname(entry, fullOutputPath.c_str());
        //
        r = archive_write_header(ext, entry);
        if (r < ARCHIVE_OK)
            fprintf(stderr, "%s\n", archive_error_string(ext));
        else if (archive_entry_size(entry) > 0) {
            r = copy_data(a, ext);
        if (r < ARCHIVE_OK)
            fprintf(stderr, "%s\n", archive_error_string(ext));
        if (r < ARCHIVE_WARN)
            return 1;
        }
        r = archive_write_finish_entry(ext);
        if (r < ARCHIVE_OK)
            fprintf(stderr, "%s\n", archive_error_string(ext));
        if (r < ARCHIVE_WARN)
            return 1;
        emit attemptUpdateProBarValue(countDcms());
    }
    archive_read_close(a);
    archive_read_free(a);
    archive_write_close(ext);
    archive_write_free(ext);
    return 0;
}

void Unpacker::run()
{
    // std::chrono::steady_clock::time_point begin = std::chrono::steady_clock::now();
    std::string filenameAbsPath = configHandler->getTgzFilePath();

    logger->info("Unpacking dataset from {}", filenameAbsPath);

    emit attemptUpdateText("Unpacking images");
    emit attemptUpdateProBarBounds(0, expected_num_files);
    emit attemptUpdateProBarValue(0);
    if (configHandler->getDatasetType() == "full_set") {
        std::filesystem::create_directory(folderAbsPath);
        extract(filenameAbsPath.c_str(), folderAbsPath);
        emit attemptUpdateProBarValue(countDcms());
    } else {
        extract(filenameAbsPath.c_str(), configHandler->getParentFolder());
    }

    // std::chrono::steady_clock::time_point end = std::chrono::steady_clock::now();
    // std::cout << "Time difference = " << (std::chrono::duration_cast<std::chrono::nanoseconds> (end - begin).count())/1000000000.0 << "[s]" << std::endl;
    emit attemptUpdateProBarValue(countDcms());
    emit attemptUpdateText("Images unpacked");
    emit finished();

    logger->info("Done unpacking");
}

quint64 Unpacker::countDcms()
{
    quint64 count = 0;
    for (auto & p : std::filesystem::recursive_directory_iterator(folderAbsPath)) {
        if (p.path().extension() == ".dcm") {
            count++;
        }
    }
    return count;
}
