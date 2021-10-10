package runnable

import (
	"CxrClassify/configHandler"
	"CxrClassify/databaseHandler"
	"CxrClassify/expectedSizes"

	"github.com/therecipe/qt/core"
)

type Runnable struct {
	ConfigHandler   *configHandler.ConfigHandler
	DatabaseHandler *databaseHandler.DatabaseHandler

	Expected_size      int
	Expected_num_files int

	Qr *core.QRunnable
	// core.QObject
}

// func (d Downloader) QRunnable_PTR() *core.QRunnable {
// 	return d.r.Qr
// }

func NewRunnable(configHandler *configHandler.ConfigHandler, databaseHandler *databaseHandler.DatabaseHandler) *Runnable {
	r := new(Runnable)
	// r.Qr = core.NewQRunnable()
	r.ConfigHandler = configHandler
	r.DatabaseHandler = databaseHandler
	r.Expected_num_files = expectedSizes.Expected_num_files_in_dataset[r.ConfigHandler.GetDatasetType()]
	r.Expected_size = expectedSizes.Expected_sizes[r.ConfigHandler.GetDatasetType()]
	return r
}
