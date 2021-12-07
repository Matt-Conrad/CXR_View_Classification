package trainStage

import (
	"CxrClassify/configHandler"
	"CxrClassify/databaseHandler"
	"CxrClassify/stage"
)

type TrainStage struct {
	stage.Stage

	Trainer *Trainer

	_ func() `constructor:"init"`
}

func (t *TrainStage) init() {

}

func (t *TrainStage) Setup(configHandler *configHandler.ConfigHandler, databaseHandler *databaseHandler.DatabaseHandler) {
	t.Trainer = NewTrainer(nil)
	t.Trainer.Setup(configHandler, databaseHandler)
}

func (t *TrainStage) Train() {
	t.Trainer.Run()
}
