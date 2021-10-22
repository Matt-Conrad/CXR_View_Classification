package downloadStage

import (
	"CxrClassify/configHandler"
	"CxrClassify/databaseHandler"
	"CxrClassify/downloader"
	"CxrClassify/stage"
)

type DownloadStage struct {
	stage.Stage

	Downloader *downloader.Downloader

	_ func() `constructor:"init"`
}

func (d *DownloadStage) init() {

}

func (d *DownloadStage) Setup(configHandler *configHandler.ConfigHandler, databaseHandler *databaseHandler.DatabaseHandler) {
	d.Downloader = downloader.NewDownloader(nil)
	d.Downloader.Setup(configHandler, databaseHandler)
}

func (d *DownloadStage) Download() {
	d.Downloader.Run()
}
