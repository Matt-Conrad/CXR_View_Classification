package storeStage

import (
	"CxrClassify/configHandler"
	"CxrClassify/databaseHandler"
	"CxrClassify/stage"
	"CxrClassify/storer"
)

type StoreStage struct {
	stage.Stage

	Storer *storer.Storer

	_ func() `constructor:"init"`
}

func (s *StoreStage) init() {

}

func (s *StoreStage) Setup(configHandler *configHandler.ConfigHandler, databaseHandler *databaseHandler.DatabaseHandler) {
	s.Storer = storer.NewStorer(nil)
	s.Storer.Setup(configHandler, databaseHandler)
}

func (s *StoreStage) Store() {
	s.Storer.Run()
}
