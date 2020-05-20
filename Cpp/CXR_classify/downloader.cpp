#include "downloader.h"

Downloader::Downloader(std::string url, std::string filename_fullpath) : QObject()
{
    Downloader::url = url;
    Downloader::filename_fullpath = filename_fullpath;
}

void Downloader::getDataset()
{
    if (std::filesystem::exists(filename_fullpath) && !std::filesystem::is_directory(filename_fullpath)) {
        if (std::filesystem::file_size(filename_fullpath) == expected_size) {
            std::cout << "File  was downloaded properly" << std::endl;
        } else {
            std::filesystem::remove(filename_fullpath);
            Downloader::downloadDataset();
        }
    } else {
        Downloader::downloadDataset();
    }
    emit finished();
}

void Downloader::downloadDataset()
{
    download();
}

static size_t write_data(void *ptr, size_t size, size_t nmemb, void *stream)
{
  size_t written = fwrite(ptr, size, nmemb, (FILE *)stream);
  return written;
}

int Downloader::download()
{
    CURL *curl_handle;
    static const char *pagefilename = filename_fullpath.c_str();
    FILE *pagefile;

    curl_global_init(CURL_GLOBAL_ALL);

    /* init the curl session */
    curl_handle = curl_easy_init();

    /* set URL to get here */
    curl_easy_setopt(curl_handle, CURLOPT_URL, url.c_str());

    /* Switch on full protocol/debug output while testing */
    curl_easy_setopt(curl_handle, CURLOPT_VERBOSE, 1L);

    /* disable progress meter, set to 0L to enable and disable debug output */
    curl_easy_setopt(curl_handle, CURLOPT_NOPROGRESS, 1L);

    /* send all data to this function  */
    curl_easy_setopt(curl_handle, CURLOPT_WRITEFUNCTION, write_data);

    /* open the file */
    pagefile = fopen(pagefilename, "wb");
    if(pagefile) {

        /* write the page body to this file handle */
        curl_easy_setopt(curl_handle, CURLOPT_WRITEDATA, pagefile);

        /* get it! */
        curl_easy_perform(curl_handle);

        /* close the header file */
        fclose(pagefile);
    }

    /* cleanup curl stuff */
    curl_easy_cleanup(curl_handle);

    curl_global_cleanup();

    return 0;
}
