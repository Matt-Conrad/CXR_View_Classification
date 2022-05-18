package downloadStage

import (
	"CxrClassify/configHandler"
	"CxrClassify/databaseHandler"
	"CxrClassify/runnable"
	"fmt"
	"log"
	"time"

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
	k, err := os.OpenFile("testlogfile", os.O_RDWR|os.O_CREATE|os.O_APPEND, 0666)
	if err != nil {
		log.Fatalf("error opening file: %v", err)
	}
	defer k.Close()
	log.SetOutput(k)

	log.Println("Checking if {} already exists")
	info, err := os.Stat(d.FilenameAbsPath)
	if err == nil && !info.IsDir() {
		log.Println("{} already exists")
		log.Println("Checking if {} was downloaded properly")
		if info.Size() == int64(d.Expected_size) {
			log.Println("{} was downloaded properly")
			d.AttemptUpdateText("Image download complete")
			d.Finished()
		} else {
			log.Println("{} was not downloaded properly")
			log.Println("Removing {}")
			e := os.Remove(d.FilenameAbsPath)
			if e != nil {
				log.Println("FAILED")
			}
			log.Println("Successfully removed {}")
		}
	} else {
		log.Println("{} does not exist")

		log.Printf("Downloading dataset from: %s", d.ConfigHandler.GetUrl())

		d.AttemptUpdateText("Downloading images")
		d.AttemptUpdateProBarBounds(0, int(d.getTgzMax()))

		go d.download()

		go func() {

			exists := false
			for !exists {
				_, error := os.Stat("NLMCXR_subset_dataset.tgz")

				// check if error is "file not exists"
				if os.IsNotExist(error) {
					log.Printf("file does not exist\n")
				} else {
					log.Printf("file exist\n")
					exists = true
				}
			}

			var downloaded int64 = -1
			for downloaded < d.getTgzMax() {
				downloaded = d.getTgzSize()
				d.AttemptUpdateProBarValue(int(downloaded))
				time.Sleep(time.Second)
			}

			d.AttemptUpdateText("Image download complete")
			d.Finished()
		}()
	}
}

func (d Downloader) download() error {
	// Create the file
	out, err := os.Create(d.FilenameAbsPath)
	if err != nil {
		return err
	}
	defer out.Close()

	// Get the data
	resp, err := http.Get(d.ConfigHandler.GetUrl())
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	// Check server response
	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("unexpected error code")
	}

	_, err = io.Copy(out, resp.Body)
	if err != nil {
		return err
	}

	return nil
}

func (d Downloader) getTgzSize() int64 {
	fi, err := os.Stat(d.FilenameAbsPath)
	if err != nil {
		log.Println("5")
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
