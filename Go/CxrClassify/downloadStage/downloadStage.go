package downloadStage

import (
	"CxrClassify/configHandler"
	"CxrClassify/downloader"
	"CxrClassify/stage"
)

type DownloadStage struct {
	downloader *downloader.Downloader
	s          *stage.Stage
}

func NewDownloadStage(configHandler *configHandler.ConfigHandler) *DownloadStage {
	ds := new(DownloadStage)
	ds.s = stage.NewStage()
	ds.downloader = downloader.NewDownloader(configHandler)

	return ds
}

func (ds DownloadStage) Download() {
	ds.downloader.Run()
}
