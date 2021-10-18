package unpackStage

import (
	"CxrClassify/configHandler"
	"CxrClassify/stage"
	"CxrClassify/unpacker"
)

type UnpackStage struct {
	stage.Stage

	Unpacker *unpacker.Unpacker

	_ func() `constructor:"init"`
}

func (u *UnpackStage) init() {

}

func (u *UnpackStage) Setup(configHandler *configHandler.ConfigHandler) {
	u.Unpacker = unpacker.NewUnpacker(nil)
	u.Unpacker.Setup(configHandler)
}

func (u *UnpackStage) Unpack() {
	u.Unpacker.Run()
}
