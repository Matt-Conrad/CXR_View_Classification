package trainStage

import (
	"CxrClassify/configHandler"
	"CxrClassify/databaseHandler"
	"CxrClassify/stage"
	"CxrClassify/trainer"
)

type TrainStage struct {
	stage.Stage

	Trainer *trainer.Trainer

	_ func() `constructor:"init"`
}

func (t *TrainStage) init() {

}

func (t *TrainStage) Setup(configHandler *configHandler.ConfigHandler, databaseHandler *databaseHandler.DatabaseHandler) {
	t.Trainer = trainer.NewTrainer(nil)
	t.Trainer.Setup(configHandler, databaseHandler)
}

func (t *TrainStage) Train() {
	t.Trainer.Run()
}
