package featureCalculator

import (
	"CxrClassify/configHandler"
	"CxrClassify/databaseHandler"
	"CxrClassify/runnable"
)

type FeatureCalculator struct {
	runnable.Runnable

	_ func() `constructor:"init"`
}

func (f *FeatureCalculator) init() {

}

func (f *FeatureCalculator) Setup(configHandler *configHandler.ConfigHandler, databaseHandler *databaseHandler.DatabaseHandler) {
	f.SetupRunnable(configHandler, databaseHandler)
}

func (f FeatureCalculator) Run() {

}
