package mainWindow

import (
	"CxrClassify/configHandler"
	"CxrClassify/databaseHandler"
	"os"

	"github.com/therecipe/qt/core"
	"github.com/therecipe/qt/widgets"
)

type MainWindow struct {
	configHandler *configHandler.ConfigHandler
	dbHandler     *databaseHandler.DatabaseHandler
	window        *widgets.QMainWindow

	mainWidget  *widgets.QWidget
	widgetStack *widgets.QStackedWidget

	buttonsList [6]string
}

func NewMainWindow() *MainWindow {
	m := new(MainWindow)

	m.configHandler = configHandler.NewConfigHandler("./config.ini")

	// Add logging

	m.dbHandler = databaseHandler.NewDatabaseHandler(m.configHandler)

	// TODO: Move this into the struct
	m.buttonsList = [6]string{"downloadBtn", "unpackBtn", "storeBtn", "featureBtn", "labelBtn", "trainBtn"}

	m.window = widgets.NewQMainWindow(nil, 0)
	m.window.SetWindowTitle("CXR Classifier Training Walkthrough")

	m.fillWindow()
	m.initGuiState()
	m.window.Show()

	return m
}

func (m MainWindow) Close() {
	defer m.configHandler.Close()
}

func (m *MainWindow) fillWindow() {
	// Create widget for the dashboard
	dashboardWidget := widgets.NewQWidget(nil, 0)

	msgBox := widgets.NewQLabel(nil, 0)
	proBar := widgets.NewQProgressBar(nil)

	msgBox.SetObjectName("msgBox")
	proBar.SetObjectName("proBar")

	dashboardLayout := widgets.NewQGridLayout(nil)
	dashboardLayout.AddWidget3(msgBox, 1, 0, 1, 3, 0)
	dashboardLayout.AddWidget3(proBar, 2, 0, 1, 3, 0)

	dashboardWidget.SetLayout(dashboardLayout)

	// Create widget for the stage buttons
	stagesWidget := widgets.NewQWidget(m.mainWidget, 0)

	downloadBtn := widgets.NewQPushButton2("Download", nil)
	unpackBtn := widgets.NewQPushButton2("Unpack", nil)
	storeBtn := widgets.NewQPushButton2("Store Metadata", nil)
	featureBtn := widgets.NewQPushButton2("Calculate Features", nil)
	labelBtn := widgets.NewQPushButton2("Label Images", nil)
	trainBtn := widgets.NewQPushButton2("Train Classifier", nil)

	downloadBtn.SetObjectName("downloadBtn")
	unpackBtn.SetObjectName("unpackBtn")
	storeBtn.SetObjectName("storeBtn")
	featureBtn.SetObjectName("featureBtn")
	labelBtn.SetObjectName("labelBtn")
	trainBtn.SetObjectName("trainBtn")

	stagesLayout := widgets.NewQGridLayout(nil)
	stagesLayout.AddWidget2(downloadBtn, 1, 0, 0)
	stagesLayout.AddWidget2(unpackBtn, 1, 1, 0)
	stagesLayout.AddWidget2(storeBtn, 1, 2, 0)
	stagesLayout.AddWidget2(featureBtn, 2, 0, 0)
	stagesLayout.AddWidget2(labelBtn, 2, 1, 0)
	stagesLayout.AddWidget2(trainBtn, 2, 2, 0)

	stagesWidget.SetLayout(stagesLayout)

	// Create widget for the labeler
	labelerWidget := widgets.NewQWidget(nil, 0)

	image := widgets.NewQLabel(nil, 0)
	image.SetAlignment(core.Qt__AlignCenter)
	frontalBtn := widgets.NewQPushButton2("Frontal", nil)
	lateralBtn := widgets.NewQPushButton2("Lateral", nil)

	image.SetObjectName("image")
	frontalBtn.SetObjectName("frontalBtn")
	lateralBtn.SetObjectName("lateralBtn")

	labelLayout := widgets.NewQGridLayout(nil)
	labelLayout.AddWidget3(image, 1, 0, 1, 2, 0)
	labelLayout.AddWidget2(frontalBtn, 2, 0, 0)
	labelLayout.AddWidget2(lateralBtn, 2, 1, 0)

	labelerWidget.SetLayout(labelLayout)

	// Set up widget stack
	widgetStack := widgets.NewQStackedWidget(nil)
	widgetStack.AddWidget(stagesWidget)
	widgetStack.AddWidget(labelerWidget)

	// Full stack
	m.mainWidget = widgets.NewQWidget(nil, 0)
	mainLayout := widgets.NewQVBoxLayout()
	mainLayout.AddWidget(dashboardWidget, 0, 0)
	mainLayout.AddWidget(widgetStack, 0, 0)
	m.mainWidget.SetLayout(mainLayout)

	m.window.SetCentralWidget(m.mainWidget)
}

func (m MainWindow) initGuiState() {
	// TODO: add setwindowicon

	// m.downloadStageUi()

	if m.dbHandler.TableExists(m.configHandler.GetTableName("label")) {
		m.trainStageUi()
	} else if m.dbHandler.TableExists(m.configHandler.GetTableName("features")) {
		m.labelStageUi()
	} else if m.dbHandler.TableExists(m.configHandler.GetTableName("metadata")) {
		m.calcFeatStageUi()
	} else if _, err := os.Stat(m.configHandler.GetUnpackFolderPath()); err == nil {
		m.storeStageUi()
	} else if _, err := os.Stat(m.configHandler.GetTgzFilename()); err == nil {
		m.unpackStageUi()
	} else {
		m.downloadStageUi()
	}
}

func (m MainWindow) downloadStageUi() {
	m.disableAllStageButtons()
	m.enableStageButton(0)

	widgets.NewQPushButtonFromPointer(m.mainWidget.FindChild("downloadBtn", core.Qt__FindChildrenRecursively).Pointer()).ConnectClicked(func(checked bool) {
		m.unpackStageUi()
	})
}

func (m MainWindow) unpackStageUi() {
	m.disableAllStageButtons()
	m.enableStageButton(1)

	widgets.NewQPushButtonFromPointer(m.mainWidget.FindChild("unpackBtn", core.Qt__FindChildrenRecursively).Pointer()).ConnectClicked(func(checked bool) {
		m.storeStageUi()
	})
}

func (m MainWindow) storeStageUi() {
	m.disableAllStageButtons()
	m.enableStageButton(2)

	widgets.NewQPushButtonFromPointer(m.mainWidget.FindChild("storeBtn", core.Qt__FindChildrenRecursively).Pointer()).ConnectClicked(func(checked bool) {
		m.calcFeatStageUi()
	})
}

func (m MainWindow) calcFeatStageUi() {
	m.disableAllStageButtons()
	m.enableStageButton(3)

	widgets.NewQPushButtonFromPointer(m.mainWidget.FindChild("featureBtn", core.Qt__FindChildrenRecursively).Pointer()).ConnectClicked(func(checked bool) {
		m.labelStageUi()
	})
}

func (m MainWindow) labelStageUi() {
	m.disableAllStageButtons()
	m.enableStageButton(4)

	widgets.NewQPushButtonFromPointer(m.mainWidget.FindChild("labelBtn", core.Qt__FindChildrenRecursively).Pointer()).ConnectClicked(func(checked bool) {
		m.trainStageUi()
	})
}

func (m MainWindow) trainStageUi() {
	m.disableAllStageButtons()
	m.enableStageButton(5)
}

// func (m MainWindow) clearCurrentStage() {
// 	defer currentStage.Close()
// }

func (m MainWindow) firstPage() {
	m.widgetStack.SetCurrentIndex(0)
}

func (m MainWindow) secondPage() {
	m.widgetStack.SetCurrentIndex(1)
}

// func (m MainWindow) connectToDashboard() {

// }

func (m MainWindow) disableAllStageButtons() {
	numOfButtons := len(m.buttonsList)
	for i := 0; i < numOfButtons; i++ {
		widgets.NewQPushButtonFromPointer(m.mainWidget.FindChild(m.buttonsList[i], core.Qt__FindChildrenRecursively).Pointer()).SetDisabled(true)
	}
}

func (m MainWindow) enableStageButton(stageIndex int) {
	widgets.NewQPushButtonFromPointer(m.mainWidget.FindChild(m.buttonsList[stageIndex], core.Qt__FindChildrenRecursively).Pointer()).SetDisabled(false)
}

func (m MainWindow) updateText(text string) {
	widgets.NewQLabelFromPointer(m.mainWidget.FindChild("msgBox", core.Qt__FindChildrenRecursively).Pointer()).SetText(text)
}

func (m MainWindow) updateProBarBounds(proBarMin, proBarMax int) {
	widgets.NewQProgressBarFromPointer(m.mainWidget.FindChild("proBar", core.Qt__FindChildrenRecursively).Pointer()).SetMinimum(proBarMin)
	widgets.NewQProgressBarFromPointer(m.mainWidget.FindChild("proBar", core.Qt__FindChildrenRecursively).Pointer()).SetMaximum(proBarMax)
}

func (m MainWindow) updateProBarValue(value int) {
	widgets.NewQProgressBarFromPointer(m.mainWidget.FindChild("proBar", core.Qt__FindChildrenRecursively).Pointer()).SetValue(value)
}

// func (m MainWindow) updateImage(text string) {
// TODO
// }
