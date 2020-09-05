import logging
from PyQt5.QtCore import pyqtSlot, QThread, Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QMainWindow, QWidget, QProgressBar, QLabel, QPushButton, QStackedWidget, QGridLayout
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

        self.fill_window()
        self.show()
        
        logging.info('Done constructing Main app')

    def fill_window(self):
        """Fills the window with buttons."""
        self.setWindowTitle("CXR Classifier Training Walkthrough")

        # Create widget for the stage buttons
        stagesWidget = QWidget()

        msg_box = QLabel('Welcome to the CXR Classification Application', self)
        pro_bar = QProgressBar(self)
        download_btn = QPushButton("Download", self)
        unpack_btn = QPushButton("Unpack", self)
        store_btn = QPushButton("Store Metadata", self)
        features_btn = QPushButton("Calculate Features", self)
        label_btn = QPushButton("Label Images", self)
        classify_btn = QPushButton("Train Classifier", self)

        msg_box.setObjectName("msg_box")
        pro_bar.setObjectName("pro_bar")
        download_btn.setObjectName("download_btn")
        unpack_btn.setObjectName("unpack_btn")
        store_btn.setObjectName("store_btn")
        features_btn.setObjectName("features_btn")
        label_btn.setObjectName("label_btn")
        classify_btn.setObjectName("classify_btn")
        
        full_layout = QGridLayout()
        full_layout.addWidget(msg_box, 1, 0, 1, 3)
        full_layout.addWidget(pro_bar, 2, 0, 1, 3)
        full_layout.addWidget(download_btn, 3, 0)
        full_layout.addWidget(unpack_btn, 3, 1)
        full_layout.addWidget(store_btn, 3, 2)
        full_layout.addWidget(features_btn, 4, 0)
        full_layout.addWidget(label_btn, 4, 1)
        full_layout.addWidget(classify_btn, 4, 2)

        stagesWidget.setLayout(full_layout)

        # Create widget for the labeler
        labelWidget = QWidget()

        labelerMsgBox = QLabel()
        labelerProBar = QProgressBar(self)
        image = QLabel(self)
        image.setAlignment(Qt.AlignCenter)
        frontal_btn = QPushButton('Frontal', self)
        lateral_btn = QPushButton('Lateral', self)

        labelerMsgBox.setObjectName("labelerMsgBox")
        labelerProBar.setObjectName("labelerProBar")
        image.setObjectName("image")
        frontal_btn.setObjectName("frontal_btn")
        lateral_btn.setObjectName("lateral_btn")

        labelLayout = QGridLayout()
        labelLayout.addWidget(labelerMsgBox, 1, 0, 1, 2)
        labelLayout.addWidget(labelerProBar, 2, 0, 1, 2)
        labelLayout.addWidget(image, 3, 0, 1, 2)
        labelLayout.addWidget(frontal_btn, 4, 0)
        labelLayout.addWidget(lateral_btn, 4, 1)

        labelWidget.setLayout(labelLayout)
        
        # Set up widget stack
        self.widgetStack = QStackedWidget()
        self.widgetStack.addWidget(stagesWidget)
        self.widgetStack.addWidget(labelWidget)

        self.setCentralWidget(self.widgetStack)

    @pyqtSlot(int)
    def update_pro_bar_val(self, value):
        self.widgetStack.widget(0).findChild(QProgressBar, "pro_bar").setValue(value)
        self.widgetStack.widget(1).findChild(QProgressBar, "labelerProBar").setValue(value)

    @pyqtSlot(int, int)
    def update_pro_bar_bounds(self, proBarMin, proBarMax):
        self.widgetStack.widget(0).findChild(QProgressBar, "pro_bar").setMinimum(proBarMin)
        self.widgetStack.widget(0).findChild(QProgressBar, "pro_bar").setMaximum(proBarMax)
        self.widgetStack.widget(1).findChild(QProgressBar, "labelerProBar").setMinimum(proBarMin)
        self.widgetStack.widget(1).findChild(QProgressBar, "labelerProBar").setMaximum(proBarMax)

    @pyqtSlot(str)
    def update_text(self, text):
        self.widgetStack.widget(0).findChild(QLabel, "msg_box").setText(text)
        self.widgetStack.widget(1).findChild(QLabel, "labelerMsgBox").setText(text)

    @pyqtSlot(object)
    def updateImage(self, record):
        image = pdm.dcmread(record['file_path']).pixel_array
        bits_stored = record['bits_stored']
        pixmap = self.arr_into_pixmap(image, bits_stored)
        self.widgetStack.widget(1).findChild(QLabel, "image").setPixmap(pixmap)

    @pyqtSlot()
    def stage1_ui(self):
        logging.info('Window initializing in Download phase')
        self.widgetStack.widget(0).findChild(QPushButton, "download_btn").setDisabled(False)
        self.widgetStack.widget(0).findChild(QPushButton, "unpack_btn").setDisabled(True)
        self.widgetStack.widget(0).findChild(QPushButton, "store_btn").setDisabled(True)
        self.widgetStack.widget(0).findChild(QPushButton, "features_btn").setDisabled(True)
        self.widgetStack.widget(0).findChild(QPushButton, "label_btn").setDisabled(True)
        self.widgetStack.widget(0).findChild(QPushButton, "classify_btn").setDisabled(True)

        self.widgetStack.widget(0).findChild(QPushButton, "download_btn").clicked.connect(self.controller.downloader.checkDatasetStatus)

        self.connectToDashboard(self.controller.downloader)

        self.controller.downloader.finished.connect(self.stage2_ui)
        self.controller.downloader.finished.connect(self.controller.downloader.deleteLater)

        logging.info('***Download phase initialized***')

    @pyqtSlot()
    def stage2_ui(self):
        logging.info('Window initializing in Unpack phase')
        self.widgetStack.widget(0).findChild(QPushButton, "download_btn").setDisabled(True)
        self.widgetStack.widget(0).findChild(QPushButton, "unpack_btn").setDisabled(False)
        self.widgetStack.widget(0).findChild(QPushButton, "store_btn").setDisabled(True)
        self.widgetStack.widget(0).findChild(QPushButton, "features_btn").setDisabled(True)
        self.widgetStack.widget(0).findChild(QPushButton, "label_btn").setDisabled(True)
        self.widgetStack.widget(0).findChild(QPushButton, "classify_btn").setDisabled(True)

        self.unpacker = Unpacker(self.controller.configHandler)
        self.unpackUpdater = UnpackUpdater(self.controller.configHandler)

        # Unpacker
        self.unpackThread = QThread()
        self.unpacker.moveToThread(self.unpackThread)
        self.widgetStack.widget(0).findChild(QPushButton, "unpack_btn").clicked.connect(self.unpackThread.start)
        self.unpackThread.started.connect(self.unpacker.unpack)

        # Unpack Updater
        self.unpackUpdaterThread = QThread()
        self.unpackUpdater.moveToThread(self.unpackUpdaterThread)
        self.widgetStack.widget(0).findChild(QPushButton, "unpack_btn").clicked.connect(self.unpackUpdaterThread.start)
        self.unpackUpdaterThread.started.connect(self.unpackUpdater.update)

        self.connectToDashboard(self.unpackUpdater)
        
        self.unpacker.finished.connect(self.unpackThread.quit)
        self.unpackUpdater.finished.connect(self.unpackUpdaterThread.quit)

        self.unpackThread.finished.connect(self.unpackThread.deleteLater)
        self.unpackUpdaterThread.finished.connect(self.unpackUpdaterThread.deleteLater)

        self.unpackUpdater.finished.connect(self.stage3_ui)
        logging.info('***Unpack phase initialized***')
        
    @pyqtSlot()
    def stage3_ui(self):
        logging.info('Window initializing in Store phase')
        self.widgetStack.widget(0).findChild(QPushButton, "download_btn").setDisabled(True)
        self.widgetStack.widget(0).findChild(QPushButton, "unpack_btn").setDisabled(True)
        self.widgetStack.widget(0).findChild(QPushButton, "store_btn").setDisabled(False)
        self.widgetStack.widget(0).findChild(QPushButton, "features_btn").setDisabled(True)
        self.widgetStack.widget(0).findChild(QPushButton, "label_btn").setDisabled(True)
        self.widgetStack.widget(0).findChild(QPushButton, "classify_btn").setDisabled(True)

        self.storer = Storer(self.controller.configHandler, self.controller.dbHandler)
        self.storeUpdater = StoreUpdater(self.controller.configHandler, self.controller.dbHandler)

        # Storer
        self.storeThread = QThread()
        self.storer.moveToThread(self.storeThread)
        self.widgetStack.widget(0).findChild(QPushButton, "store_btn").clicked.connect(self.storeThread.start)
        self.storeThread.started.connect(self.storer.store)

        # Store Updater
        self.storeUpdaterThread = QThread()
        self.storeUpdater.moveToThread(self.storeUpdaterThread)
        self.widgetStack.widget(0).findChild(QPushButton, "store_btn").clicked.connect(self.storeUpdaterThread.start)
        self.storeUpdaterThread.started.connect(self.storeUpdater.update)

        self.connectToDashboard(self.storeUpdater)

        self.storer.finished.connect(self.storeThread.quit)
        self.storeUpdater.finished.connect(self.storeUpdaterThread.quit)

        self.storeThread.finished.connect(self.storeThread.deleteLater)
        self.storeUpdaterThread.finished.connect(self.storeUpdaterThread.deleteLater)

        self.storeUpdater.finished.connect(self.stage4_ui)
        logging.info('***Store phase initialized***')

    @pyqtSlot()
    def stage4_ui(self):
        logging.info('Window initializing in Feature Calculation phase')
        self.widgetStack.widget(0).findChild(QPushButton, "download_btn").setDisabled(True)
        self.widgetStack.widget(0).findChild(QPushButton, "unpack_btn").setDisabled(True)
        self.widgetStack.widget(0).findChild(QPushButton, "store_btn").setDisabled(True)
        self.widgetStack.widget(0).findChild(QPushButton, "features_btn").setDisabled(False)
        self.widgetStack.widget(0).findChild(QPushButton, "label_btn").setDisabled(True)
        self.widgetStack.widget(0).findChild(QPushButton, "classify_btn").setDisabled(True)

        self.widgetStack.widget(0).findChild(QPushButton, "features_btn").clicked.connect(self.controller.featCalc.calculate_features)

        self.connectToDashboard(self.controller.featCalc)

        self.controller.featCalc.finished.connect(self.stage5_ui)
        self.controller.featCalc.finished.connect(self.controller.featCalc.deleteLater)
        logging.info('***Feature Calculation phase initialized***')

    @pyqtSlot()
    def stage5_ui(self):
        logging.info('Window initializing in Labeling phase')
        self.widgetStack.widget(0).findChild(QPushButton, "download_btn").setDisabled(True)
        self.widgetStack.widget(0).findChild(QPushButton, "unpack_btn").setDisabled(True)
        self.widgetStack.widget(0).findChild(QPushButton, "store_btn").setDisabled(True)
        self.widgetStack.widget(0).findChild(QPushButton, "features_btn").setDisabled(True)
        self.widgetStack.widget(0).findChild(QPushButton, "label_btn").setDisabled(False)
        self.widgetStack.widget(0).findChild(QPushButton, "classify_btn").setDisabled(True)

        if self.controller.configHandler.getDatasetType() == 'subset':
            self.widgetStack.widget(0).findChild(QPushButton, "label_btn").clicked.connect(lambda: self.centralWidget().setCurrentIndex(1))
            self.widgetStack.widget(0).findChild(QPushButton, "label_btn").clicked.connect(self.controller.labeler.startLabeler)

            self.widgetStack.widget(1).findChild(QPushButton, "frontal_btn").clicked.connect(self.controller.labeler.frontal)
            self.widgetStack.widget(1).findChild(QPushButton, "lateral_btn").clicked.connect(self.controller.labeler.lateral)
            self.controller.labeler.attemptUpdateImage.connect(self.updateImage)

            self.connectToDashboard(self.controller.labeler)
            self.controller.labeler.finished.connect(lambda: self.centralWidget().setCurrentIndex(0))
            self.controller.labeler.finished.connect(self.stage6_ui)
            self.controller.labeler.finished.connect(self.controller.labeler.deleteLater)

        elif self.controller.configHandler.getDatasetType() == 'full_set':
            self.widgetStack.widget(0).findChild(QPushButton, "label_btn").clicked.connect(self.controller.label_importer.importLabels)
            self.connectToDashboard(self.controller.label_importer)
            self.controller.label_importer.finished.connect(self.stage6_ui)
            self.controller.label_importer.finished.connect(self.controller.label_importer.deleteLater)
        else:
            raise ValueError('Value must be one of the keys in SOURCE_URL')
        logging.info('***Labeling phase initialized***')

    @pyqtSlot()
    def stage6_ui(self):
        logging.info('Window initializing in Training phase')
        self.setFixedSize(self.centralWidget().currentWidget().layout().sizeHint())

        self.widgetStack.widget(0).findChild(QPushButton, "download_btn").setDisabled(True)
        self.widgetStack.widget(0).findChild(QPushButton, "unpack_btn").setDisabled(True)
        self.widgetStack.widget(0).findChild(QPushButton, "store_btn").setDisabled(True)
        self.widgetStack.widget(0).findChild(QPushButton, "features_btn").setDisabled(True)
        self.widgetStack.widget(0).findChild(QPushButton, "label_btn").setDisabled(True)
        self.widgetStack.widget(0).findChild(QPushButton, "classify_btn").setDisabled(False)

        self.widgetStack.widget(0).findChild(QPushButton, "classify_btn").clicked.connect(self.controller.trainer.train)

        self.connectToDashboard(self.controller.trainer)

        self.controller.trainer.finished.connect(self.controller.trainer.deleteLater)
        logging.info('***Training phase initialized***')

    def connectToDashboard(self, stage):
        stage.attemptUpdateProBarBounds.connect(self.update_pro_bar_bounds)
        stage.attemptUpdateProBarValue.connect(self.update_pro_bar_val)
        stage.attemptUpdateText.connect(self.update_text)

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
