package unpackStage

import (
	"CxrClassify/configHandler"
	"CxrClassify/databaseHandler"
	"CxrClassify/stage"
)

type UnpackStage struct {
	stage.Stage

	Unpacker *Unpacker

	_ func() `constructor:"init"`
}

func (u *UnpackStage) init() {

}

func (u *UnpackStage) Setup(configHandler *configHandler.ConfigHandler, databaseHandler *databaseHandler.DatabaseHandler) {
	u.Unpacker = NewUnpacker(nil)
	u.Unpacker.Setup(configHandler, databaseHandler)
}

func (u *UnpackStage) Unpack() {
	u.Unpacker.Run()
}
