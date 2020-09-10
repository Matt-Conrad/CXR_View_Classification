import logging
from PyQt5.QtCore import pyqtSlot, QThread, Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow, QWidget, QProgressBar, QLabel, QPushButton, QStackedWidget, QGridLayout, QVBoxLayout
import pydicom as pdm
import cv2
import numpy as np

class MainWindow(QMainWindow):
    """Contains GUI code for the application."""
    def __init__(self, controller):
        logging.info('Constructing Main app')
        QMainWindow.__init__(self, windowTitle="CXR Classifier Training Walkthrough")
        self.controller = controller

        self.buttons_list = ["download_btn", "unpack_btn", "store_btn", "features_btn", "label_btn", "classify_btn"]

        self.fill_window()
        self.show()
        
        logging.info('Done constructing Main app')

    def fill_window(self):
        """Fills the window with buttons."""
        # Create widget for the dashboard
        dashboardWidget = QWidget()

        msg_box = QLabel('Welcome to the CXR Classification Application', objectName="msg_box")
        pro_bar = QProgressBar(objectName="pro_bar")

        dashboardLayout = QGridLayout()
        dashboardLayout.addWidget(msg_box, 1, 0, 1, 3)
        dashboardLayout.addWidget(pro_bar, 2, 0, 1, 3)

        dashboardWidget.setLayout(dashboardLayout)

        # Create widget for the stage buttons
        stagesWidget = QWidget()

        download_btn = QPushButton("Download", objectName="download_btn", clicked=self.controller.downloadStage.download)
        unpack_btn = QPushButton("Unpack", objectName="unpack_btn", clicked=self.controller.unpackStage.unpack)
        store_btn = QPushButton("Store Metadata", objectName="store_btn", clicked=self.controller.storeStage.store)
        features_btn = QPushButton("Calculate Features", objectName="features_btn", clicked=self.controller.featCalcStage.calculateFeatures)
        label_btn = QPushButton("Label Images", objectName="label_btn")
        classify_btn = QPushButton("Train Classifier", objectName="classify_btn", clicked=self.controller.trainStage.train)
        
        stagesLayout = QGridLayout()
        stagesLayout.addWidget(download_btn, 1, 0)
        stagesLayout.addWidget(unpack_btn, 1, 1)
        stagesLayout.addWidget(store_btn, 1, 2)
        stagesLayout.addWidget(features_btn, 2, 0)
        stagesLayout.addWidget(label_btn, 2, 1)
        stagesLayout.addWidget(classify_btn, 2, 2)

        stagesWidget.setLayout(stagesLayout)

        # Create widget for the labeler
        labelerWidget = QWidget()

        image = QLabel(objectName="image")
        image.setAlignment(Qt.AlignCenter)
        frontal_btn = QPushButton('Frontal', objectName="frontal_btn", clicked=self.controller.labelerStage.labeler.frontal)
        lateral_btn = QPushButton('Lateral', objectName="lateral_btn", clicked=self.controller.labelerStage.labeler.lateral)

        labelLayout = QGridLayout()
        labelLayout.addWidget(image, 1, 0, 1, 2)
        labelLayout.addWidget(frontal_btn, 2, 0)
        labelLayout.addWidget(lateral_btn, 2, 1)

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

    @pyqtSlot(int)
    def update_pro_bar_val(self, value):
        self.centralWidget().findChild(QProgressBar, "pro_bar").setValue(value)

    @pyqtSlot(int, int)
    def update_pro_bar_bounds(self, proBarMin, proBarMax):
        self.centralWidget().findChild(QProgressBar, "pro_bar").setMinimum(proBarMin)
        self.centralWidget().findChild(QProgressBar, "pro_bar").setMaximum(proBarMax)

    @pyqtSlot(str)
    def update_text(self, text):
        self.centralWidget().findChild(QLabel, "msg_box").setText(text)

    @pyqtSlot(object)
    def updateImage(self, record):
        image = pdm.dcmread(record['file_path']).pixel_array
        bits_stored = record['bits_stored']
        pixmap = self.arr_into_pixmap(image, bits_stored)
        self.widgetStack.currentWidget().findChild(QLabel, "image").setPixmap(pixmap)

    @pyqtSlot()
    def downloadStageUi(self):
        logging.info('Window initializing in Download phase')
        self.disableAllStageButtons()
        self.enableStageButton(0)

        self.connectToDashboard(self.controller.downloadStage.downloader.signals)

        self.controller.downloadStage.downloader.signals.finished.connect(self.unpackStageUi)
        logging.info('***Download phase initialized***')

    @pyqtSlot()
    def unpackStageUi(self):
        logging.info('Window initializing in Unpack phase')
        self.disableAllStageButtons()
        self.enableStageButton(1)

        self.connectToDashboard(self.controller.unpackStage.unpackUpdater.signals)

        self.controller.unpackStage.unpackUpdater.signals.finished.connect(self.storeStageUi)
        logging.info('***Unpack phase initialized***')
        
    @pyqtSlot()
    def storeStageUi(self):
        logging.info('Window initializing in Store phase')
        self.disableAllStageButtons()
        self.enableStageButton(2)

        self.connectToDashboard(self.controller.storeStage.storeUpdater.signals)

        self.controller.storeStage.storeUpdater.signals.finished.connect(self.calcFeatStageUi)
        logging.info('***Store phase initialized***')

    @pyqtSlot()
    def calcFeatStageUi(self):
        logging.info('Window initializing in Feature Calculation phase')
        self.disableAllStageButtons()
        self.enableStageButton(3)

        self.connectToDashboard(self.controller.featCalcStage.featureCalculator.signals)

        self.controller.featCalcStage.featureCalculator.signals.finished.connect(self.labelStageUi)
        logging.info('***Feature Calculation phase initialized***')

    @pyqtSlot()
    def labelStageUi(self):
        logging.info('Window initializing in Labeling phase')
        self.disableAllStageButtons()
        self.enableStageButton(4)

        if self.controller.configHandler.getDatasetType() == 'subset':
            self.centralWidget().findChild(QPushButton, "label_btn").clicked.connect(lambda: self.widgetStack.setCurrentIndex(1))
            self.centralWidget().findChild(QPushButton, "label_btn").clicked.connect(self.controller.labelerStage.label)

            self.controller.labelerStage.labeler.signals.attemptUpdateImage.connect(self.updateImage)

            self.connectToDashboard(self.controller.labelerStage.labeler.signals)
            self.controller.labelerStage.labeler.signals.finished.connect(lambda: self.widgetStack.setCurrentIndex(0))
            self.controller.labelerStage.labeler.signals.finished.connect(self.trainStageUi)

        elif self.controller.configHandler.getDatasetType() == 'full_set':
            self.centralWidget().findChild(QPushButton, "label_btn").clicked.connect(self.controller.labelImporterStage.importLabels)
            self.connectToDashboard(self.controller.labelImporterStage.labelImporter.signals)
            self.controller.labelImporterStage.labelImporter.signals.finished.connect(self.trainStageUi)
        else:
            raise ValueError('Value must be one of the keys in SOURCE_URL')
        logging.info('***Labeling phase initialized***')

    @pyqtSlot()
    def trainStageUi(self):
        logging.info('Window initializing in Training phase')
        self.widgetStack.setFixedSize(self.widgetStack.currentWidget().layout().sizeHint())
        self.setFixedSize(self.centralWidget().layout().sizeHint())

        self.disableAllStageButtons()
        self.enableStageButton(5)

        self.connectToDashboard(self.controller.trainStage.trainer.signals)
        logging.info('***Training phase initialized***')

    def connectToDashboard(self, signals):
        signals.attemptUpdateProBarBounds.connect(self.update_pro_bar_bounds)
        signals.attemptUpdateProBarValue.connect(self.update_pro_bar_val)
        signals.attemptUpdateText.connect(self.update_text)

    def disableAllStageButtons(self):
        for button in self.buttons_list:
            self.centralWidget().findChild(QPushButton, button).setDisabled(True)

    def enableStageButton(self, stageIndex):
        self.centralWidget().findChild(QPushButton, self.buttons_list[stageIndex]).setDisabled(False)

    def arr_into_pixmap(self, image, bits_stored):
        """Convert the image array into a QPixmap for display."""
        # Scale the pixel intensity to uint8
        highest_possible_intensity = (np.power(2, bits_stored) - 1)
        image = (image/highest_possible_intensity * 255).astype(np.uint8)

        image = cv2.resize(image, (300,300), interpolation=cv2.INTER_AREA)

        height, width = image.shape
        bytes_per_line = width
        q_image = QImage(image, width, height, bytes_per_line, QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(q_image)

        return pixmap
