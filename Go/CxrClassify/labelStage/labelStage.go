package labelStage

import (
	"CxrClassify/configHandler"
	"CxrClassify/databaseHandler"
	"CxrClassify/manualLabeler"
	"CxrClassify/stage"
)

type LabelStage struct {
	stage.Stage

	ManualLabeler *manualLabeler.ManualLabeler

	_ func() `constructor:"init"`
}

func (l *LabelStage) init() {

}

func (l *LabelStage) Setup(configHandler *configHandler.ConfigHandler, databaseHandler *databaseHandler.DatabaseHandler) {
	l.ManualLabeler = manualLabeler.NewManualLabeler(nil)
	l.ManualLabeler.Setup(configHandler, databaseHandler)
}

func (l *LabelStage) Label() {
	l.ManualLabeler.Run()
}
