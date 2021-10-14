package downloadStage

import (
	"CxrClassify/configHandler"
	"CxrClassify/downloader"
	"CxrClassify/stage"
)

type DownloadStage struct {
	stage.Stage

	Downloader *downloader.Downloader

	_ func() `slot:"Download"`

	_ func() `constructor:"init"`
}

func (d *DownloadStage) init() {

}

func (d *DownloadStage) Setup(configHandler *configHandler.ConfigHandler) {
	d.Downloader = downloader.NewDownloader(nil)
	d.Downloader.Setup(configHandler)
}

func (d *DownloadStage) DownloadData() {
	d.Downloader.Run()
}
