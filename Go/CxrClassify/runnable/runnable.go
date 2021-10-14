package runnable

import (
	"CxrClassify/configHandler"
	"CxrClassify/databaseHandler"
	"CxrClassify/expectedSizes"

	"github.com/therecipe/qt/core"
)

type Runnable struct {
	core.QObject
	// core.QRunnable

	_ func(*configHandler.ConfigHandler) `constructor:"init"`

	ConfigHandler   *configHandler.ConfigHandler
	DatabaseHandler *databaseHandler.DatabaseHandler

	Expected_size      int
	Expected_num_files int

	_ func()         `signal:"finished"`
	_ func(int)      `signal:"attemptUpdateProBarValue"`
	_ func(int, int) `signal:"attemptUpdateProBarBounds"`
	_ func(string)   `signal:"attemptUpdateText"`

	// _ *configHandler.ConfigHandler `property:"configHandler"`
}

func (r *Runnable) init() {

}

func (r *Runnable) SetupRunnable(configHandler *configHandler.ConfigHandler) {
	r.ConfigHandler = configHandler
	r.Expected_num_files = expectedSizes.Expected_num_files_in_dataset[r.ConfigHandler.GetDatasetType()]
	r.Expected_size = expectedSizes.Expected_sizes[r.ConfigHandler.GetDatasetType()]
}
