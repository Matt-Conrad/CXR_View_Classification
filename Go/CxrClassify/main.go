package main

// REQUIRES export GO111module=off

import (
	"os"

	"CxrClassify/mainWindow"

	"github.com/therecipe/qt/widgets"
)

func main() {
	// Temporary set up
	app := widgets.NewQApplication(len(os.Args), os.Args)

	mainWindow.NewMainWindow(nil, 0)

	// defer m.Close()

	// start the main Qt event loop
	// and block until app.Exit() is called
	// or the window is closed by the user
	app.Exec()
}
