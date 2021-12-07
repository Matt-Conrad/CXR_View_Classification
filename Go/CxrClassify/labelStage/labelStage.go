package labelStage

import (
	"CxrClassify/configHandler"
	"CxrClassify/databaseHandler"
	"CxrClassify/stage"
)

type LabelStage struct {
	stage.Stage

	ManualLabeler *ManualLabeler

	_ func() `constructor:"init"`
}

func (l *LabelStage) init() {

}

func (l *LabelStage) Setup(configHandler *configHandler.ConfigHandler, databaseHandler *databaseHandler.DatabaseHandler) {
	l.ManualLabeler = NewManualLabeler(nil)
	l.ManualLabeler.Setup(configHandler, databaseHandler)
}

func (l *LabelStage) Label() {
	l.ManualLabeler.Run()
}
