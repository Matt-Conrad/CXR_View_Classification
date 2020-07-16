#include "unpacker.h"

Unpacker::Unpacker(ConfigHandler * configHandler) : QObject()
{
    Unpacker::configHandler = configHandler;

    Unpacker::expected_num_files = expected_num_files_in_dataset.at(configHandler->getTgzFilename());
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

void Unpacker::unpack()
{
    std::string filename_fullpath = configHandler->getParentFolder() + "/" + configHandler->getTgzFilename();
    std::string folder_full_path = configHandler->getParentFolder() + "/" + configHandler->getDatasetName();

    emit attemptUpdateText("Unpacking images");
    emit attemptUpdateProBarBounds(0, expected_num_files);
    emit attemptUpdateProBarValue(0);
    if (configHandler->getDatasetType() == "full_set") {
        std::filesystem::create_directory(folder_full_path);
        extract(filename_fullpath.c_str(), folder_full_path);
        emit attemptUpdateProBarValue(countDcms());
    } else {
        extract(filename_fullpath.c_str(), configHandler->getParentFolder());
    }
    emit attemptUpdateProBarValue(countDcms());
    emit attemptUpdateText("Images unpacked");
    emit finished();
}

quint64 Unpacker::countDcms()
{
    std::string folder_full_path = configHandler->getParentFolder() + "/" + configHandler->getDatasetName();

    quint64 count = 0;
    for (auto & p : std::filesystem::recursive_directory_iterator(folder_full_path)) {
        if (p.path().extension() == ".dcm") {
            count++;
        }
    }
    return count;
}
