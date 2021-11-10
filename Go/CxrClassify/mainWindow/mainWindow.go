package mainWindow

import (
	"CxrClassify/configHandler"
	"CxrClassify/databaseHandler"
	"CxrClassify/downloadStage"
	"CxrClassify/trainStage"
	"image"
	"log"

	"CxrClassify/featStage"
	"CxrClassify/labelStage"
	"CxrClassify/stage"
	"CxrClassify/storeStage"
	"CxrClassify/unpackStage"
	"os"

	"github.com/therecipe/qt/core"
	"github.com/therecipe/qt/gui"
	"github.com/therecipe/qt/widgets"
	"gocv.io/x/gocv"
)

type MainWindow struct {
	widgets.QMainWindow

	configHandler *configHandler.ConfigHandler
	dbHandler     *databaseHandler.DatabaseHandler
	window        *widgets.QMainWindow

	mainWidget  *widgets.QWidget
	widgetStack *widgets.QStackedWidget

	buttonsList [6]string

	_ func() `constructor:"init"`

	_ func(int, int)    `slot:"updateProBarBounds"`
	_ func(int)         `slot:"updateProBarValue"`
	_ func(string)      `slot:"updateText"`
	_ func(gui.QPixmap) `slot:"updateImage"`

	downloadStage          *downloadStage.DownloadStage
	unpackStage            *unpackStage.UnpackStage
	storeStage             *storeStage.StoreStage
	featureCalculatorStage *featStage.FeatStage
	labelStage             *labelStage.LabelStage
	trainStage             *trainStage.TrainStage

	// currentStage []stage.StageInterface
}

func (m *MainWindow) init() {
	k, err := os.OpenFile("testlogfile", os.O_RDWR|os.O_CREATE|os.O_APPEND, 0666)
	if err != nil {
		log.Fatalf("error opening file: %v", err)
	}
	defer k.Close()
	log.SetOutput(k)

	m.configHandler = configHandler.NewConfigHandler("./config.ini")

	// Add logging

	m.dbHandler = databaseHandler.NewDatabaseHandler(m.configHandler)

	// TODO: Move this into the struct
	m.buttonsList = [6]string{"downloadBtn", "unpackBtn", "storeBtn", "featureBtn", "labelBtn", "trainBtn"}

	m.SetWindowTitle("CXR Classifier Training Walkthrough")

	m.fillWindow()
	m.initGuiState()
	m.Show()
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
	m.widgetStack = widgets.NewQStackedWidget(nil)
	m.widgetStack.AddWidget(stagesWidget)
	m.widgetStack.AddWidget(labelerWidget)

	// Full stack
	m.mainWidget = widgets.NewQWidget(nil, 0)
	mainLayout := widgets.NewQVBoxLayout()
	mainLayout.AddWidget(dashboardWidget, 0, 0)
	mainLayout.AddWidget(m.widgetStack, 0, 0)
	m.mainWidget.SetLayout(mainLayout)

	m.SetCentralWidget(m.mainWidget)
}

func (m MainWindow) initGuiState() {
	// TODO: add setwindowicon

	// TODO: figure out why it's not unpacking to binary location
	// unpackFilePath := m.configHandler.GetUnpackFolderPath() + m.configHandler.GetTgzFilename()

	// m.updateText(m.configHandler.GetUnpackFolderPath())

	if m.dbHandler.TableExists(m.configHandler.GetTableName("label")) {
		m.trainStageUi()
	} else if m.dbHandler.TableExists(m.configHandler.GetTableName("features")) {
		m.labelStageUi()
	} else if m.dbHandler.TableExists(m.configHandler.GetTableName("metadata")) {
		m.calcFeatStageUi()
	} else if _, err := os.Stat(m.configHandler.GetUnpackFolderPath()); err == nil {
		m.storeStageUi()
	} else if _, err := os.Stat(m.configHandler.GetTgzFilePath()); err == nil {
		m.unpackStageUi()
	} else {
		m.downloadStageUi()
	}
}

func (m MainWindow) downloadStageUi() {
	m.downloadStage = downloadStage.NewDownloadStage(nil)
	m.downloadStage.Setup(m.configHandler, m.dbHandler)

	// m.currentStage = []stage.StageInterface{&downloadStage.DownloadStage{}}

	m.disableAllStageButtons()
	m.enableStageButton(0)

	widgets.NewQPushButtonFromPointer(m.mainWidget.FindChild("downloadBtn", core.Qt__FindChildrenRecursively).Pointer()).ConnectClicked(func(checked bool) {
		m.downloadStage.Download()
	})

	m.connectToDashboard(m.downloadStage.Downloader)
	m.downloadStage.Downloader.ConnectFinished(m.unpackStageUi)
}

func (m MainWindow) unpackStageUi() {
	m.unpackStage = unpackStage.NewUnpackStage(nil)
	m.unpackStage.Setup(m.configHandler, m.dbHandler)

	m.disableAllStageButtons()
	m.enableStageButton(1)

	widgets.NewQPushButtonFromPointer(m.mainWidget.FindChild("unpackBtn", core.Qt__FindChildrenRecursively).Pointer()).ConnectClicked(func(checked bool) {
		m.unpackStage.Unpack()
	})

	m.connectToDashboard(m.unpackStage.Unpacker)
	m.unpackStage.Unpacker.ConnectFinished(m.storeStageUi)
}

func (m MainWindow) storeStageUi() {
	m.storeStage = storeStage.NewStoreStage(nil)
	m.storeStage.Setup(m.configHandler, m.dbHandler)

	m.disableAllStageButtons()
	m.enableStageButton(2)

	widgets.NewQPushButtonFromPointer(m.mainWidget.FindChild("storeBtn", core.Qt__FindChildrenRecursively).Pointer()).ConnectClicked(func(checked bool) {
		m.storeStage.Store()
	})

	m.connectToDashboard(m.storeStage.Storer)
	m.storeStage.Storer.ConnectFinished(m.calcFeatStageUi)
}

func (m MainWindow) calcFeatStageUi() {
	m.featureCalculatorStage = featStage.NewFeatStage(nil)
	m.featureCalculatorStage.Setup(m.configHandler, m.dbHandler)

	m.disableAllStageButtons()
	m.enableStageButton(3)

	widgets.NewQPushButtonFromPointer(m.mainWidget.FindChild("featureBtn", core.Qt__FindChildrenRecursively).Pointer()).ConnectClicked(func(checked bool) {
		m.featureCalculatorStage.CalculateFeatures()
	})

	m.connectToDashboard(m.featureCalculatorStage.FeatureCalculator)
	m.featureCalculatorStage.FeatureCalculator.ConnectFinished(m.labelStageUi)
}

func (m MainWindow) labelStageUi() {
	m.labelStage = labelStage.NewLabelStage(nil)
	m.labelStage.Setup(m.configHandler, m.dbHandler)

	m.disableAllStageButtons()
	m.enableStageButton(4)

	widgets.NewQPushButtonFromPointer(m.mainWidget.FindChild("labelBtn", core.Qt__FindChildrenRecursively).Pointer()).ConnectClicked(func(checked bool) {
		m.labelStage.Label()
	})

	widgets.NewQPushButtonFromPointer(m.widgetStack.FindChild("frontalBtn", core.Qt__FindChildrenRecursively).Pointer()).ConnectClicked(func(checked bool) {
		m.labelStage.ManualLabeler.Frontal()
	})

	widgets.NewQPushButtonFromPointer(m.widgetStack.FindChild("lateralBtn", core.Qt__FindChildrenRecursively).Pointer()).ConnectClicked(func(checked bool) {
		m.labelStage.ManualLabeler.Lateral()
	})

	widgets.NewQPushButtonFromPointer(m.mainWidget.FindChild("labelBtn", core.Qt__FindChildrenRecursively).Pointer()).ConnectClicked(func(checked bool) {
		m.secondPage()
	})

	m.connectToDashboard(m.labelStage.ManualLabeler)
	m.labelStage.ManualLabeler.ConnectFinished(m.firstPage)
	m.labelStage.ManualLabeler.ConnectFinished(m.trainStageUi)
}

func (m MainWindow) trainStageUi() {
	m.trainStage = trainStage.NewTrainStage(nil)
	m.trainStage.Setup(m.configHandler, m.dbHandler)

	m.widgetStack.SetFixedSize(m.widgetStack.CurrentWidget().SizeHint())
	m.SetFixedSize(m.CentralWidget().SizeHint())

	m.disableAllStageButtons()
	m.enableStageButton(5)

	widgets.NewQPushButtonFromPointer(m.mainWidget.FindChild("trainBtn", core.Qt__FindChildrenRecursively).Pointer()).ConnectClicked(func(checked bool) {
		m.trainStage.Train()
	})

	m.connectToDashboard(m.trainStage.Trainer)

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

func (m MainWindow) connectToDashboard(test stage.StageInterface) {
	test.ConnectAttemptUpdateProBarBounds(m.updateProBarBounds)
	test.ConnectAttemptUpdateProBarValue(m.updateProBarValue)
	test.ConnectAttemptUpdateText(m.updateText)
	test.ConnectAttemptUpdateImage(m.updateImage)
}

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

func (m MainWindow) updateImage(filePath string) {
	originalImage := gocv.IMRead(filePath, gocv.IMReadGrayScale)
	imageSquare := gocv.NewMatWithSize(300, 300, gocv.MatTypeCV8U)
	gocv.Resize(originalImage, &imageSquare, image.Pt(300, 300), 0, 0, gocv.InterpolationArea)

	imageData, _ := gocv.IMEncode(".jpg", imageSquare)
	qImage := gui.NewQImage()
	qImage.LoadFromData(imageData.GetBytes(), len(imageData.GetBytes()), "JPG")

	qPixmap := gui.NewQPixmap().FromImage(qImage, 0)

	widgets.NewQLabelFromPointer(m.mainWidget.FindChild("image", core.Qt__FindChildrenRecursively).Pointer()).SetPixmap(qPixmap)
}
