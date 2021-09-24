package mainWindow

import (
	"CxrClassify/configHandler"
	"CxrClassify/databaseHandler"
	// "github.com/therecipe/qt/widgets"
)

type MainWindow struct {
	configHandler   *configHandler.ConfigHandler
	databaseHandler *databaseHandler.DatabaseHandler
}

func NewMainWindow() *MainWindow {
	m := new(MainWindow)
	m.configHandler = new(configHandler.ConfigHandler)
	m.databaseHandler = new(databaseHandler.DatabaseHandler)
}
