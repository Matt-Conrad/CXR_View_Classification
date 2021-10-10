package downloader

import (
	"CxrClassify/configHandler"
	"CxrClassify/runnable"
	"fmt"
	"io"
	"net/http"
	"os"
)

type Downloader struct {
	filenameAbsPath string
	datasetType     string
	r               runnable.Runnable
}

func NewDownloader(configHandler *configHandler.ConfigHandler) *Downloader {
	d := new(Downloader)
	d.filenameAbsPath = configHandler.GetTgzFilePath()
	d.datasetType = configHandler.GetDatasetType()
	d.r = *runnable.NewRunnable(configHandler, nil)

	return d
}

// func (d Downloader) QRunnable_PTR() *core.QRunnable {
// 	return d.r.Qr
// }

func (d Downloader) Run() {
	fmt.Println("Checking if {} already exists")
	info, err := os.Stat(d.filenameAbsPath)
	if err == nil && !info.IsDir() {
		fmt.Println("{} already exists")
		fmt.Println("Checking if {} was downloaded properly")
		if info.Size() == int64(d.r.Expected_size) {
			fmt.Println("{} was downloaded properly")
		} else {
			fmt.Println("{} was not downloaded properly")
			fmt.Println("Removing {}")
			e := os.Remove(d.filenameAbsPath)
			if e != nil {
				fmt.Println("FAILED")
			}
			fmt.Println("Successfully removed {}")
			d.download()
		}
	} else {
		fmt.Println("{} does not exist")
		d.download()
	}
}

func (d Downloader) download() int {
	// Create the file
	out, err := os.Create(d.filenameAbsPath)
	if err != nil {
		fmt.Println("1")
		return 1
	}
	defer out.Close()

	// Get the data
	resp, err := http.Get(d.r.ConfigHandler.GetUrl())
	if err != nil {
		fmt.Println("2")
		return 1
	}
	defer resp.Body.Close()

	// Check server response
	if resp.StatusCode != http.StatusOK {
		fmt.Println("3")
		return 1
	}

	// Writer the body to file
	_, err = io.Copy(out, resp.Body)
	if err != nil {
		fmt.Println("4")
		return 1
	}

	return 0
}

func (d Downloader) getTgzSize() int64 {
	fi, err := os.Stat(d.filenameAbsPath)
	if err != nil {
		fmt.Println("5")
	}

	if d.datasetType == "full_set" {
		return int64(fi.Size() / 100)
	} else if d.datasetType == "subset" {
		return fi.Size()
	} else {
		return 0
	}
}

func (d Downloader) getTgzMax() int64 {
	if d.datasetType == "full_set" {
		return int64(d.r.Expected_size / 100)
	} else if d.datasetType == "subset" {
		return int64(d.r.Expected_size)
	} else {
		return 0
	}
}
