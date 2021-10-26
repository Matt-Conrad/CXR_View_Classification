package featStage

import (
	"CxrClassify/configHandler"
	"CxrClassify/databaseHandler"
	"CxrClassify/featureCalculator"
	"CxrClassify/stage"
)

type FeatStage struct {
	stage.Stage

	FeatureCalculator *featureCalculator.FeatureCalculator

	_ func() `constructor:"init"`
}

func (f *FeatStage) init() {

}

func (f *FeatStage) Setup(configHandler *configHandler.ConfigHandler, databaseHandler *databaseHandler.DatabaseHandler) {
	f.FeatureCalculator = featureCalculator.NewFeatureCalculator(nil)
	f.FeatureCalculator.Setup(configHandler, databaseHandler)
}

func (f *FeatStage) CalculateFeatures() {
	f.FeatureCalculator.Run()
}
