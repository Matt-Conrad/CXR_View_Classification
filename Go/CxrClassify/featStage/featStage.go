package featStage

import (
	"CxrClassify/configHandler"
	"CxrClassify/databaseHandler"
	"CxrClassify/stage"
)

type FeatStage struct {
	stage.Stage

	FeatureCalculator *FeatureCalculator

	_ func() `constructor:"init"`
}

func (f *FeatStage) init() {

}

func (f *FeatStage) Setup(configHandler *configHandler.ConfigHandler, databaseHandler *databaseHandler.DatabaseHandler) {
	f.FeatureCalculator = NewFeatureCalculator(nil)
	f.FeatureCalculator.Setup(configHandler, databaseHandler)
}

func (f *FeatStage) CalculateFeatures() {
	f.FeatureCalculator.Run()
}
