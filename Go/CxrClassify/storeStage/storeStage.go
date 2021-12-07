package storeStage

import (
	"CxrClassify/configHandler"
	"CxrClassify/databaseHandler"
	"CxrClassify/stage"
)

type StoreStage struct {
	stage.Stage

	Storer *Storer

	_ func() `constructor:"init"`
}

func (s *StoreStage) init() {

}

func (s *StoreStage) Setup(configHandler *configHandler.ConfigHandler, databaseHandler *databaseHandler.DatabaseHandler) {
	s.Storer = NewStorer(nil)
	s.Storer.Setup(configHandler, databaseHandler)
}

func (s *StoreStage) Store() {
	s.Storer.Run()
}
