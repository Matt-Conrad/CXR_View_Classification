import logging
import os
import pydicom as pdm
import cv2
import numpy as np
from PyQt5.QtCore import pyqtSlot, QThread, Qt
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QProgressBar, QLabel, QPushButton, QStackedWidget, QGridLayout, QVBoxLayout

import logging
from downloadStage import DownloadStage
from unpackStage import UnpackStage
from storeStage import StoreStage
from featureCalculatorStage import FeatCalcStage
from labelStage import LabelStage
from trainStage import TrainStage
from cxrConfigHandler import CxrConfigHandler
from metadata_to_db.databaseHandler import DatabaseHandler

class MainWindow(QMainWindow):
    """Contains GUI code for the application."""
    def __init__(self):
        parentFolder = os.path.dirname(os.path.abspath(__file__))
        self.configHandler = CxrConfigHandler(os.path.join(parentFolder, "config.ini"))
        self.configureLogging()

        logging.info('Constructing Main app')
        QMainWindow.__init__(self, windowTitle="CXR Classifier Training Walkthrough")
        
        self.dbHandler = DatabaseHandler(self.configHandler)

        self.buttonsList = ["downloadBtn", "unpackBtn", "storeBtn", "featureBtn", "labelBtn", "classifyBtn"]
        self.currentStage = None

        self.fillWindow()
        self.initGuiState()
        self.show()
        
        logging.info('Done constructing Main app')

    def fillWindow(self):
        """Fills the window with buttons."""
        # Create widget for the dashboard
        dashboardWidget = QWidget()

        msgBox = QLabel('Welcome to the CXR Classification Application', objectName="msgBox")
        proBar = QProgressBar(objectName="proBar")

        dashboardLayout = QGridLayout()
        dashboardLayout.addWidget(msgBox, 1, 0, 1, 3)
        dashboardLayout.addWidget(proBar, 2, 0, 1, 3)

        dashboardWidget.setLayout(dashboardLayout)

        # Create widget for the stage buttons
        stagesWidget = QWidget()

        downloadBtn = QPushButton("Download", objectName="downloadBtn")
        unpackBtn = QPushButton("Unpack", objectName="unpackBtn")
        storeBtn = QPushButton("Store Metadata", objectName="storeBtn")
        featureBtn = QPushButton("Calculate Features", objectName="featureBtn")
        labelBtn = QPushButton("Label Images", objectName="labelBtn")
        classifyBtn = QPushButton("Train Classifier", objectName="classifyBtn")
        
        stagesLayout = QGridLayout()
        stagesLayout.addWidget(downloadBtn, 1, 0)
        stagesLayout.addWidget(unpackBtn, 1, 1)
        stagesLayout.addWidget(storeBtn, 1, 2)
        stagesLayout.addWidget(featureBtn, 2, 0)
        stagesLayout.addWidget(labelBtn, 2, 1)
        stagesLayout.addWidget(classifyBtn, 2, 2)

        stagesWidget.setLayout(stagesLayout)

        # Create widget for the labeler
        labelerWidget = QWidget()

        image = QLabel(objectName="image")
        image.setAlignment(Qt.AlignCenter)
        frontalBtn = QPushButton('Frontal', objectName="frontalBtn")
        lateralBtn = QPushButton('Lateral', objectName="lateralBtn")

        labelLayout = QGridLayout()
        labelLayout.addWidget(image, 1, 0, 1, 2)
        labelLayout.addWidget(frontalBtn, 2, 0)
        labelLayout.addWidget(lateralBtn, 2, 1)

        labelerWidget.setLayout(labelLayout)
        
        # Set up widget stack
        self.widgetStack = QStackedWidget()
        self.widgetStack.addWidget(stagesWidget)
        self.widgetStack.addWidget(labelerWidget)

        # Full stack
        self.mainWidget = QWidget()
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(dashboardWidget)
        mainLayout.addWidget(self.widgetStack)
        self.mainWidget.setLayout(mainLayout)

        self.setCentralWidget(self.mainWidget)

    ### STAGES UI
    def initGuiState(self):
        self.setWindowIcon(QIcon(os.path.join(self.configHandler.getParentFolder(), 'icon.jpg')))

        # Initialize in right stage
        if self.dbHandler.tableExists(self.configHandler.getTableName("label")):
            self.trainStageUi()
        elif self.dbHandler.tableExists(self.configHandler.getTableName("features")):
            self.labelStageUi()
        elif self.dbHandler.tableExists(self.configHandler.getTableName("metadata")):
            self.calcFeatStageUi()
        elif os.path.isdir(self.configHandler.getDatasetName()):
            self.storeStageUi()
        elif os.path.exists(self.configHandler.getTgzFilename()):
            self.unpackStageUi()
        else:
            self.downloadStageUi()
            
    @pyqtSlot()
    def downloadStageUi(self):
        logging.info('Window initializing in Download phase')
        self.currentStage = DownloadStage(self.configHandler)

        self.disableAllStageButtons()
        self.enableStageButton(0)

        self.connectToDashboard(self.currentStage.downloader.signals)
        
        self.centralWidget().findChild(QPushButton, "downloadBtn").clicked.connect(self.currentStage.download)
        self.currentStage.downloader.signals.finished.connect(self.unpackStageUi)
        logging.info('***Download phase initialized***')

    @pyqtSlot()
    def unpackStageUi(self):
        logging.info('Window initializing in Unpack phase')
        self.currentStage = UnpackStage(self.configHandler)

        self.disableAllStageButtons()
        self.enableStageButton(1)

        self.connectToDashboard(self.currentStage.unpackUpdater.signals)

        self.centralWidget().findChild(QPushButton, "unpackBtn").clicked.connect(self.currentStage.unpack)
        self.currentStage.unpackUpdater.signals.finished.connect(self.storeStageUi)
        logging.info('***Unpack phase initialized***')
        
    @pyqtSlot()
    def storeStageUi(self):
        logging.info('Window initializing in Store phase')
        self.currentStage = StoreStage(self.configHandler, self.dbHandler)

        self.disableAllStageButtons()
        self.enableStageButton(2)

        self.connectToDashboard(self.currentStage.storeUpdater.signals)

        self.centralWidget().findChild(QPushButton, "storeBtn").clicked.connect(self.currentStage.store)
        self.currentStage.storeUpdater.signals.finished.connect(self.calcFeatStageUi)
        logging.info('***Store phase initialized***')

    @pyqtSlot()
    def calcFeatStageUi(self):
        logging.info('Window initializing in Feature Calculation phase')
        self.currentStage = FeatCalcStage(self.configHandler, self.dbHandler)

        self.disableAllStageButtons()
        self.enableStageButton(3)

        self.connectToDashboard(self.currentStage.featureCalculator.signals)

        self.centralWidget().findChild(QPushButton, "featureBtn").clicked.connect(self.currentStage.calculateFeatures)
        self.currentStage.featureCalculator.signals.finished.connect(self.labelStageUi)
        logging.info('***Feature Calculation phase initialized***')

    @pyqtSlot()
    def labelStageUi(self):
        logging.info('Window initializing in Labeling phase')
        self.currentStage = LabelStage(self.configHandler, self.dbHandler)
        
        self.disableAllStageButtons()
        self.enableStageButton(4)

        self.connectToDashboard(self.currentStage.labeler.signals)

        if self.configHandler.getDatasetType() == 'subset':
            self.centralWidget().findChild(QPushButton, "labelBtn").clicked.connect(lambda: self.widgetStack.setCurrentIndex(1))
            self.widgetStack.findChild(QPushButton, "frontalBtn").clicked.connect(self.currentStage.labeler.frontal)
            self.widgetStack.findChild(QPushButton, "lateralBtn").clicked.connect(self.currentStage.labeler.lateral)
            self.currentStage.labeler.signals.finished.connect(lambda: self.widgetStack.setCurrentIndex(0))

        self.centralWidget().findChild(QPushButton, "labelBtn").clicked.connect(self.currentStage.label)
        self.currentStage.labeler.signals.finished.connect(self.trainStageUi)
        logging.info('***Labeling phase initialized***')

    @pyqtSlot()
    def trainStageUi(self):
        logging.info('Window initializing in Training phase')
        self.currentStage = TrainStage(self.configHandler, self.dbHandler)
        
        self.widgetStack.setFixedSize(self.widgetStack.currentWidget().layout().sizeHint())
        self.setFixedSize(self.centralWidget().layout().sizeHint())

        self.disableAllStageButtons()
        self.enableStageButton(5)

        self.centralWidget().findChild(QPushButton, "classifyBtn").clicked.connect(self.currentStage.train)
        self.connectToDashboard(self.currentStage.trainer.signals)
        logging.info('***Training phase initialized***')

    ### HELPERS
    @pyqtSlot(int)
    def updateProBarVal(self, value):
        self.centralWidget().findChild(QProgressBar, "proBar").setValue(value)

    @pyqtSlot(int, int)
    def updateProBarBounds(self, proBarMin, proBarMax):
        self.centralWidget().findChild(QProgressBar, "proBar").setMinimum(proBarMin)
        self.centralWidget().findChild(QProgressBar, "proBar").setMaximum(proBarMax)

    @pyqtSlot(str)
    def updateText(self, text):
        self.centralWidget().findChild(QLabel, "msgBox").setText(text)

    @pyqtSlot(object)
    def updateImage(self, record):
        print(os.getcwd()) # /mnt/hgfs/SharedFolder_Guest
        print(os.path.abspath(__file__)) # /tmp/_MEIVTMdcd/mainWindow.pyc
        image = pdm.dcmread(os.path.join(self.configHandler.getParentFolder(), record['file_path'])).pixel_array
        bitsStored = record['bits_stored']
        pixmap = self.arrIntoPixmap(image, bitsStored)
        self.widgetStack.findChild(QLabel, "image").setPixmap(pixmap)

    def connectToDashboard(self, signals):
        signals.attemptUpdateProBarBounds.connect(self.updateProBarBounds)
        signals.attemptUpdateProBarValue.connect(self.updateProBarVal)
        signals.attemptUpdateText.connect(self.updateText)
        signals.attemptUpdateImage.connect(self.updateImage)

    def disableAllStageButtons(self):
        for button in self.buttonsList:
            self.centralWidget().findChild(QPushButton, button).setDisabled(True)

    def enableStageButton(self, stageIndex):
        self.centralWidget().findChild(QPushButton, self.buttonsList[stageIndex]).setDisabled(False)

    def arrIntoPixmap(self, image, bitsStored):
        """Convert the image array into a QPixmap for display."""
        # Scale the pixel intensity to uint8
        highestPossibleIntensity = (np.power(2, bitsStored) - 1)
        image = (image/highestPossibleIntensity * 255).astype(np.uint8)

        image = cv2.resize(image, (300,300), interpolation=cv2.INTER_AREA)

        height, width = image.shape
        bytesPerLine = width
        qImage = QImage(image, width, height, bytesPerLine, QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(qImage)

        return pixmap

    def configureLogging(self):
        # Get log level from config file
        logLevel = self.configHandler.getLogLevel()
        if logLevel == 'debug':
            logLevelObj = logging.DEBUG
        elif logLevel == 'info':
            logLevelObj = logging.INFO
        
        # Remove any log handlers to make way for our logger
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        
        # Set the logging
        logging.basicConfig(filename='CXR_Classification.log', level=logLevelObj,
                            format='%(asctime)s %(levelname)-8s: %(message)s', datefmt='%Y-%m-%d|%H:%M:%S')

