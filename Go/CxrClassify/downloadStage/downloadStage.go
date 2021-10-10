package downloadStage

import (
	"CxrClassify/configHandler"
	"CxrClassify/databaseHandler"
	"CxrClassify/expectedSizes"
	"fmt"
	"io"
	"net/http"
	"os"

	"github.com/therecipe/qt/core"
)

type DownloadStage struct {
	core.QObject

	filenameAbsPath string
	datasetType     string

	ConfigHandler   *configHandler.ConfigHandler
	DatabaseHandler *databaseHandler.DatabaseHandler

	Expected_size      int
	Expected_num_files int
}

func NewDownloadStage(configHandler *configHandler.ConfigHandler) *DownloadStage {
	ds := new(DownloadStage)
	ds.ConfigHandler = configHandler
	ds.Expected_num_files = expectedSizes.Expected_num_files_in_dataset[ds.ConfigHandler.GetDatasetType()]
	ds.Expected_size = expectedSizes.Expected_sizes[ds.ConfigHandler.GetDatasetType()]
	ds.filenameAbsPath = ds.ConfigHandler.GetTgzFilePath()
	ds.datasetType = ds.ConfigHandler.GetDatasetType()
	return ds
}

func (d DownloadStage) Run() {
	fmt.Println("Checking if {} already exists")
	info, err := os.Stat(d.filenameAbsPath)
	if err == nil && !info.IsDir() {
		fmt.Println("{} already exists")
		fmt.Println("Checking if {} was downloaded properly")
		if info.Size() == int64(d.Expected_size) {
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

func (d DownloadStage) download() int {
	// Create the file
	out, err := os.Create(d.filenameAbsPath)
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

func (d DownloadStage) getTgzSize() int64 {
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

func (d DownloadStage) getTgzMax() int64 {
	if d.datasetType == "full_set" {
		return int64(d.Expected_size / 100)
	} else if d.datasetType == "subset" {
		return int64(d.Expected_size)
	} else {
		return 0
	}
}
