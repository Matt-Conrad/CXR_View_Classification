package main

import (
	"os"

	"github.com/therecipe/qt/widgets"
)

func main() {
	// needs to be called once before you can start using the QWidgets
	app := widgets.NewQApplication(len(os.Args), os.Args)

	// create a window
	// with a minimum size of 250*200
	// and sets the title to "Hello Widgets Example"
	window := widgets.NewQMainWindow(nil, 0)
	window.SetWindowTitle("CXR Classifier Training Walkthrough")

	// create a regular widget
	// give it a QVBoxLayout
	// and make it the central widget of the window
	dashboardWidget := widgets.NewQWidget(nil, 0)

	msgBox := widgets.NewQLabel(dashboardWidget, 0)
	proBar := widgets.NewQProgressBar(dashboardWidget)

	msgBox.SetObjectName("msgBox")
	proBar.SetObjectName("proBar")

	dashboardLayout := widgets.NewQGridLayout(dashboardWidget)
	dashboardLayout.AddWidget(msgBox)
	dashboardLayout.AddWidget(proBar)

	dashboardWidget.SetLayout(dashboardLayout)

	stagesWidget := widgets.NewQWidget()

	downloadBtn := widgets.NewQPushButton("Download")
	unpackBtn := widgets.NewQPushButton("Unpack")
	storeBtn := widgets.NewQPushButton("Store Metadata")
	featureBtn := widgets.NewQPushButton("Calculate Features")
	labelBtn := widgets.NewQPushButton("Label Images")
	trainBtn := widgets.NewQPushButton("Train Classifier")

	downloadBtn.SetObjectName("downloadBtn")
	unpackBtn.SetObjectName("unpackBtn")
	storeBtn.SetObjectName("storeBtn")
	featureBtn.SetObjectName("featureBtn")
	labelBtn.SetObjectName("labelBtn")
	trainBtn.SetObjectName("trainBtn")

	stagesLayout := widgets.NewQGridLayout()
	stagesLayout.AddWidget(downloadBtn)
	stagesLayout.AddWidget(unpackBtn)
	stagesLayout.AddWidget(storeBtn)
	stagesLayout.AddWidget(featureBtn)
	stagesLayout.AddWidget(labelBtn)
	stagesLayout.AddWidget(trainBtn)

	// widget.SetLayout(widgets.NewQVBoxLayout())
	window.SetCentralWidget(dashboardWidget)

	// // create a button
	// // connect the clicked signal
	// // and add it to the central widgets layout
	// button := widgets.NewQPushButton2("and click me!", nil)
	// button.ConnectClicked(func(bool) {
	// })
	// widget.Layout().AddWidget(button)

	// make the window visible
	window.Show()

	// start the main Qt event loop
	// and block until app.Exit() is called
	// or the window is closed by the user
	app.Exec()
}
