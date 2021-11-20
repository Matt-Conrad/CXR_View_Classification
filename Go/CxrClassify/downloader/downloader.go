package downloader

import (
	"CxrClassify/configHandler"
	"CxrClassify/databaseHandler"
	"CxrClassify/runnable"
	"log"

	"fmt"
	"io"
	"net/http"
	"os"
)

type Downloader struct {
	runnable.Runnable

	_ func() `constructor:"init"`

	FilenameAbsPath string
	DatasetType     string
}

func (d *Downloader) init() {

}

func (d *Downloader) Setup(configHandler *configHandler.ConfigHandler, databaseHandler *databaseHandler.DatabaseHandler) {
	d.FilenameAbsPath = configHandler.GetTgzFilePath()
	d.DatasetType = configHandler.GetDatasetType()
	d.SetupRunnable(configHandler, databaseHandler)
}

func (d Downloader) Run() {
	log.Println("Checking if {} already exists")
	info, err := os.Stat(d.FilenameAbsPath)
	if err == nil && !info.IsDir() {
		log.Println("{} already exists")
		log.Println("Checking if {} was downloaded properly")
		if info.Size() == int64(d.Expected_size) {
			log.Println("{} was downloaded properly")
		} else {
			log.Println("{} was not downloaded properly")
			log.Println("Removing {}")
			e := os.Remove(d.FilenameAbsPath)
			if e != nil {
				log.Println("FAILED")
			}
			log.Println("Successfully removed {}")
			d.downloadDataset()
		}
	} else {
		log.Println("{} does not exist")
		d.downloadDataset()
	}
	d.AttemptUpdateProBarValue(1)
	// d.AttemptUpdateProBarValue(int(d.getTgzSize()))
	d.AttemptUpdateText("Image download complete")
	d.Finished()
}

func (d Downloader) downloadDataset() int {
	log.Printf("Downloading dataset from: %s", d.ConfigHandler.GetUrl())

	d.AttemptUpdateText("Downloading images")
	// d.AttemptUpdateProBarBounds(0, int(d.getTgzMax()))

	d.AttemptUpdateProBarBounds(0, 1)

	// Create the file
	out, err := os.Create(d.FilenameAbsPath)
	if err != nil {
		fmt.Println("1")
		return 1
	}
	defer out.Close()

	// Get the data
	resp, err := http.Get(d.ConfigHandler.GetUrl())
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
	fi, err := os.Stat(d.FilenameAbsPath)
	if err != nil {
		fmt.Println("5")
	}

	if d.DatasetType == "full_set" {
		return int64(fi.Size() / 100)
	} else if d.DatasetType == "subset" {
		return fi.Size()
	} else {
		return 0
	}
}

func (d Downloader) getTgzMax() int64 {
	if d.DatasetType == "full_set" {
		return int64(d.Expected_size / 100)
	} else if d.DatasetType == "subset" {
		return int64(d.Expected_size)
	} else {
		return 0
	}
}
