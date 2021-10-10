package main

// import (
// 	"os"

// 	"CxrClassify/mainWindow"

// 	"github.com/therecipe/qt/widgets"
// )

// func main() {
// 	// Temporary set up
// 	app := widgets.NewQApplication(len(os.Args), os.Args)

// 	m := mainWindow.NewMainWindow()

// 	defer m.Close()

// 	// start the main Qt event loop
// 	// and block until app.Exit() is called
// 	// or the window is closed by the user
// 	app.Exec()
// }

import (
	"CxrClassify/configHandler"
	"CxrClassify/downloadStage"
)

func main() {
	var configHandler = configHandler.NewConfigHandler("./config.ini")
	var downloadStage = downloadStage.NewDownloadStage(configHandler)
	downloadStage.Download()

}
