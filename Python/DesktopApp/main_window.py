import logging
from PyQt5.QtCore import pyqtSlot, QThread, Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow, QWidget, QProgressBar, QLabel, QPushButton, QStackedWidget, QGridLayout, QVBoxLayout
from unpacker import Unpacker, UnpackUpdater
from storer import Storer, StoreUpdater
import pydicom as pdm
import cv2
import numpy as np

class MainWindow(QMainWindow):
    """Contains GUI code for the application."""
    def __init__(self, controller):
        logging.info('Constructing Main app')
        QMainWindow.__init__(self)
        self.controller = controller

        self.buttons_list = ["download_btn", "unpack_btn", "store_btn", "features_btn", "label_btn", "classify_btn"]

        self.fill_window()
        self.show()
        
        logging.info('Done constructing Main app')

    def fill_window(self):
        """Fills the window with buttons."""
        self.setWindowTitle("CXR Classifier Training Walkthrough")

        # Create widget for the dashboard
        dashboardWidget = QWidget()

        msg_box = QLabel('Welcome to the CXR Classification Application', self)
        pro_bar = QProgressBar(self)

        msg_box.setObjectName("msg_box")
        pro_bar.setObjectName("pro_bar")

        dashboardLayout = QGridLayout()
        dashboardLayout.addWidget(msg_box, 1, 0, 1, 3)
        dashboardLayout.addWidget(pro_bar, 2, 0, 1, 3)

        dashboardWidget.setLayout(dashboardLayout)

        # Create widget for the stage buttons
        stagesWidget = QWidget()

        download_btn = QPushButton("Download", self)
        unpack_btn = QPushButton("Unpack", self)
        store_btn = QPushButton("Store Metadata", self)
        features_btn = QPushButton("Calculate Features", self)
        label_btn = QPushButton("Label Images", self)
        classify_btn = QPushButton("Train Classifier", self)
        
        download_btn.setObjectName("download_btn")
        unpack_btn.setObjectName("unpack_btn")
        store_btn.setObjectName("store_btn")
        features_btn.setObjectName("features_btn")
        label_btn.setObjectName("label_btn")
        classify_btn.setObjectName("classify_btn")
        
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

        image = QLabel(self)
        image.setAlignment(Qt.AlignCenter)
        frontal_btn = QPushButton('Frontal', self)
        lateral_btn = QPushButton('Lateral', self)

        image.setObjectName("image")
        frontal_btn.setObjectName("frontal_btn")
        lateral_btn.setObjectName("lateral_btn")

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

        self.centralWidget().findChild(QPushButton, "download_btn").clicked.connect(self.controller.downloader.checkDatasetStatus)

        self.connectToDashboard(self.controller.downloader)

        self.controller.downloader.finished.connect(self.unpackStageUi)
        self.controller.downloader.finished.connect(self.controller.downloader.deleteLater)

        logging.info('***Download phase initialized***')

    @pyqtSlot()
    def unpackStageUi(self):
        logging.info('Window initializing in Unpack phase')
        self.disableAllStageButtons()
        self.enableStageButton(1)

        self.unpacker = Unpacker(self.controller.configHandler)
        self.unpackUpdater = UnpackUpdater(self.controller.configHandler)

        # Unpacker
        self.unpackThread = QThread()
        self.unpacker.moveToThread(self.unpackThread)
        self.centralWidget().findChild(QPushButton, "unpack_btn").clicked.connect(self.unpackThread.start)
        self.unpackThread.started.connect(self.unpacker.unpack)

        # Unpack Updater
        self.unpackUpdaterThread = QThread()
        self.unpackUpdater.moveToThread(self.unpackUpdaterThread)
        self.centralWidget().findChild(QPushButton, "unpack_btn").clicked.connect(self.unpackUpdaterThread.start)
        self.unpackUpdaterThread.started.connect(self.unpackUpdater.update)

        self.connectToDashboard(self.unpackUpdater)
        
        self.unpacker.finished.connect(self.unpackThread.quit)
        self.unpackUpdater.finished.connect(self.unpackUpdaterThread.quit)

        self.unpackThread.finished.connect(self.unpackThread.deleteLater)
        self.unpackUpdaterThread.finished.connect(self.unpackUpdaterThread.deleteLater)

        self.unpackUpdater.finished.connect(self.storeStageUi)
        logging.info('***Unpack phase initialized***')
        
    @pyqtSlot()
    def storeStageUi(self):
        logging.info('Window initializing in Store phase')
        self.disableAllStageButtons()
        self.enableStageButton(2)

        self.storer = Storer(self.controller.configHandler, self.controller.dbHandler)
        self.storeUpdater = StoreUpdater(self.controller.configHandler, self.controller.dbHandler)

        # Storer
        self.storeThread = QThread()
        self.storer.moveToThread(self.storeThread)
        self.centralWidget().findChild(QPushButton, "store_btn").clicked.connect(self.storeThread.start)
        self.storeThread.started.connect(self.storer.store)

        # Store Updater
        self.storeUpdaterThread = QThread()
        self.storeUpdater.moveToThread(self.storeUpdaterThread)
        self.centralWidget().findChild(QPushButton, "store_btn").clicked.connect(self.storeUpdaterThread.start)
        self.storer.startUpdating.connect(self.storeUpdater.update)

        self.connectToDashboard(self.storeUpdater)

        self.storer.finished.connect(self.storeThread.quit)
        self.storeUpdater.finished.connect(self.storeUpdaterThread.quit)

        self.storeThread.finished.connect(self.storeThread.deleteLater)
        self.storeUpdaterThread.finished.connect(self.storeUpdaterThread.deleteLater)

        self.storeUpdater.finished.connect(self.calcFeatStageUi)
        logging.info('***Store phase initialized***')

    @pyqtSlot()
    def calcFeatStageUi(self):
        logging.info('Window initializing in Feature Calculation phase')
        self.disableAllStageButtons()
        self.enableStageButton(3)

        self.centralWidget().findChild(QPushButton, "features_btn").clicked.connect(self.controller.featCalc.calculate_features)

        self.connectToDashboard(self.controller.featCalc)

        self.controller.featCalc.finished.connect(self.labelStageUi)
        self.controller.featCalc.finished.connect(self.controller.featCalc.deleteLater)
        logging.info('***Feature Calculation phase initialized***')

    @pyqtSlot()
    def labelStageUi(self):
        logging.info('Window initializing in Labeling phase')
        self.disableAllStageButtons()
        self.enableStageButton(4)

        if self.controller.configHandler.getDatasetType() == 'subset':
            self.centralWidget().findChild(QPushButton, "label_btn").clicked.connect(lambda: self.widgetStack.setCurrentIndex(1))
            self.centralWidget().findChild(QPushButton, "label_btn").clicked.connect(self.controller.labeler.startLabeler)

            self.centralWidget().findChild(QPushButton, "frontal_btn").clicked.connect(self.controller.labeler.frontal)
            self.centralWidget().findChild(QPushButton, "lateral_btn").clicked.connect(self.controller.labeler.lateral)
            self.controller.labeler.attemptUpdateImage.connect(self.updateImage)

            self.connectToDashboard(self.controller.labeler)
            test = self.centralWidget().findChild(QPushButton, "widgetStack")
            self.controller.labeler.finished.connect(lambda: self.widgetStack.setCurrentIndex(0))
            self.controller.labeler.finished.connect(self.trainStageUi)
            self.controller.labeler.finished.connect(self.controller.labeler.deleteLater)

        elif self.controller.configHandler.getDatasetType() == 'full_set':
            self.centralWidget().findChild(QPushButton, "label_btn").clicked.connect(self.controller.label_importer.importLabels)
            self.connectToDashboard(self.controller.label_importer)
            self.controller.label_importer.finished.connect(self.trainStageUi)
            self.controller.label_importer.finished.connect(self.controller.label_importer.deleteLater)
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

        self.centralWidget().findChild(QPushButton, "classify_btn").clicked.connect(self.controller.trainer.train)

        self.connectToDashboard(self.controller.trainer)

        self.controller.trainer.finished.connect(self.controller.trainer.deleteLater)
        logging.info('***Training phase initialized***')

    def connectToDashboard(self, stage):
        stage.attemptUpdateProBarBounds.connect(self.update_pro_bar_bounds)
        stage.attemptUpdateProBarValue.connect(self.update_pro_bar_val)
        stage.attemptUpdateText.connect(self.update_text)

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
