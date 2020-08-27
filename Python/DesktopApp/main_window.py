"""Contains GUI code for the application."""
import logging
from PyQt5.QtCore import pyqtSlot, QThread
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QProgressBar, QLabel, QPushButton
from unpacker import Unpacker, UnpackUpdater
from storer import Storer, StoreUpdater

class MainWindow(QMainWindow):
    """Contains GUI code for the application."""
    def __init__(self, controller):
        logging.info('Constructing Main app')
        QMainWindow.__init__(self)
        self.controller = controller
        
        # Set up GUI
        self.fill_window()
        self.show()
        
        logging.info('Done constructing Main app')

    def fill_window(self):
        """Fills the window with buttons."""
        # Create the central widget
        centralWidget = QWidget()

        # "Feedback dashboard" displays progress to the user
        self.feedback_dashboard = QVBoxLayout()
        self.msg_box = QLabel('Welcome to the CXR Classification Application')
        self.pro_bar = QProgressBar(self)
        self.feedback_dashboard.addWidget(self.msg_box)
        self.feedback_dashboard.addWidget(self.pro_bar)

        # Button array
        upper_buttons = QHBoxLayout()
        lower_buttons = QHBoxLayout()

        self.download_btn = QPushButton("Download", self)
        upper_buttons.addWidget(self.download_btn)

        self.unpack_btn = QPushButton("Unpack", self)
        upper_buttons.addWidget(self.unpack_btn)

        self.store_btn = QPushButton("Store Metadata", self)
        upper_buttons.addWidget(self.store_btn)

        self.features_btn = QPushButton("Calculate Features", self)
        lower_buttons.addWidget(self.features_btn)

        self.label_btn = QPushButton("Label Images", self)
        lower_buttons.addWidget(self.label_btn)

        self.classify_btn = QPushButton("Train Classifier", self)
        lower_buttons.addWidget(self.classify_btn)
        
        # Stack the feedback dashboard over the button array
        full_layout = QVBoxLayout()
        full_layout.addLayout(self.feedback_dashboard)
        full_layout.addLayout(upper_buttons)
        full_layout.addLayout(lower_buttons)

        centralWidget.setLayout(full_layout)
        self.setCentralWidget(centralWidget)

    @pyqtSlot(int)
    def update_pro_bar_val(self, value):
        """Updates the progress bar."""
        self.pro_bar.setValue(value)

    @pyqtSlot(int, int)
    def update_pro_bar_bounds(self, proBarMin, proBarMax):
        """Updates the progress bar."""
        self.pro_bar.setMinimum(proBarMin)
        self.pro_bar.setMaximum(proBarMax)

    @pyqtSlot(str)
    def update_text(self, text):
        """Updates the text."""
        self.msg_box.setText(text)

    @pyqtSlot()
    def stage1_ui(self):
        # User in download phase
        logging.info('Window initializing in stage 1')
        self.download_btn.setDisabled(False)
        self.unpack_btn.setDisabled(True)
        self.store_btn.setDisabled(True)
        self.features_btn.setDisabled(True)
        self.label_btn.setDisabled(True)
        self.classify_btn.setDisabled(True)

        self.download_btn.clicked.connect(self.controller.downloader.get_dataset)

        logging.debug('Thread connected to downloader')
        self.connectToDashboard(self.controller.downloader)

        logging.debug('Downloader signals connect to main thread')
        self.controller.downloader.finished.connect(self.stage2_ui)
        self.controller.downloader.finished.connect(self.controller.downloader.deleteLater)

        logging.info('***Stage 1 initialized***')

    @pyqtSlot()
    def stage2_ui(self):
        # User in unpack phase
        self.download_btn.setDisabled(True)
        self.unpack_btn.setDisabled(False)
        self.store_btn.setDisabled(True)
        self.features_btn.setDisabled(True)
        self.label_btn.setDisabled(True)
        self.classify_btn.setDisabled(True)

        self.unpacker = Unpacker(self.controller.configHandler)
        self.unpackUpdater = UnpackUpdater(self.controller.configHandler)

        # Unpacker
        self.unpackThread = QThread()
        self.unpacker.moveToThread(self.unpackThread)
        self.unpack_btn.clicked.connect(self.unpackThread.start)
        self.unpackThread.started.connect(self.unpacker.unpack)

        # Unpack Updater
        self.unpackUpdaterThread = QThread()
        self.unpackUpdater.moveToThread(self.unpackUpdaterThread)
        self.unpack_btn.clicked.connect(self.unpackUpdaterThread.start)
        self.unpackUpdaterThread.started.connect(self.unpackUpdater.update)

        self.connectToDashboard(self.unpackUpdater)
        
        self.unpacker.finished.connect(self.unpackThread.quit)
        self.unpackUpdater.finished.connect(self.unpackUpdaterThread.quit)

        self.unpackThread.finished.connect(self.unpackThread.deleteLater)
        self.unpackUpdaterThread.finished.connect(self.unpackUpdaterThread.deleteLater)

        self.unpackUpdater.finished.connect(self.stage3_ui)
        
    @pyqtSlot()
    def stage3_ui(self):
        # User in store metadata phase
        self.download_btn.setDisabled(True)
        self.unpack_btn.setDisabled(True)
        self.store_btn.setDisabled(False)
        self.features_btn.setDisabled(True)
        self.label_btn.setDisabled(True)
        self.classify_btn.setDisabled(True)

        self.storer = Storer(self.controller.configHandler, self.controller.dbHandler)
        self.storeUpdater = StoreUpdater(self.controller.configHandler, self.controller.dbHandler)

        # Storer
        self.storeThread = QThread()
        self.storer.moveToThread(self.storeThread)
        self.store_btn.clicked.connect(self.storeThread.start)
        self.storeThread.started.connect(self.storer.store)

        # Store Updater
        self.storeUpdaterThread = QThread()
        self.storeUpdater.moveToThread(self.storeUpdaterThread)
        self.store_btn.clicked.connect(self.storeUpdaterThread.start)
        self.storeUpdaterThread.started.connect(self.storeUpdater.update)

        self.connectToDashboard(self.storeUpdater)

        self.storer.finished.connect(self.storeThread.quit)
        self.storeUpdater.finished.connect(self.storeUpdaterThread.quit)

        self.storeThread.finished.connect(self.storeThread.deleteLater)
        self.storeUpdaterThread.finished.connect(self.storeUpdaterThread.deleteLater)

        self.storeUpdater.finished.connect(self.stage4_ui)

    @pyqtSlot()
    def stage4_ui(self):
        # User in calculate features phase
        self.download_btn.setDisabled(True)
        self.unpack_btn.setDisabled(True)
        self.store_btn.setDisabled(True)
        self.features_btn.setDisabled(False)
        self.label_btn.setDisabled(True)
        self.classify_btn.setDisabled(True)

        self.features_btn.clicked.connect(self.controller.featCalc.calculate_features)

        self.connectToDashboard(self.controller.featCalc)

        self.controller.featCalc.finished.connect(self.stage5_ui)
        self.controller.featCalc.finished.connect(self.controller.featCalc.deleteLater)

    @pyqtSlot()
    def stage5_ui(self):
        # User in labeling phase
        self.download_btn.setDisabled(True)
        self.unpack_btn.setDisabled(True)
        self.store_btn.setDisabled(True)
        self.features_btn.setDisabled(True)
        self.label_btn.setDisabled(False)
        self.classify_btn.setDisabled(True)

        # Set the progress region
        if self.controller.configHandler.getDatasetType() == 'subset':
            # Open new window with the labeling app
            self.label_btn.clicked.connect(self.controller.labeler.fill_window)
            self.controller.labeler.attemptUpdateText.connect(self.update_text)
            self.controller.labeler.finished.connect(self.stage6_ui)
            self.controller.labeler.finished.connect(self.controller.labeler.deleteLater)
        elif self.controller.configHandler.getDatasetType() == 'full_set':
            self.label_btn.clicked.connect(self.controller.label_importer.importLabels)
            self.connectToDashboard(self.controller.label_importer)
            self.controller.label_importer.finished.connect(self.stage6_ui)
            self.controller.label_importer.finished.connect(self.controller.label_importer.deleteLater)
        else:
            raise ValueError('Value must be one of the keys in SOURCE_URL')
        logging.info('***END LABELING PHASE***')

    @pyqtSlot()
    def stage6_ui(self):
        # User in classification phase
        self.download_btn.setDisabled(True)
        self.unpack_btn.setDisabled(True)
        self.store_btn.setDisabled(True)
        self.features_btn.setDisabled(True)
        self.label_btn.setDisabled(True)
        self.classify_btn.setDisabled(False)

        self.classify_btn.clicked.connect(self.controller.trainer.train)

        self.connectToDashboard(self.controller.trainer)

        self.controller.trainer.finished.connect(self.controller.trainer.deleteLater)

    def connectToDashboard(self, stage):
        stage.attemptUpdateProBarBounds.connect(self.update_pro_bar_bounds)
        stage.attemptUpdateProBarValue.connect(self.update_pro_bar_val)
        stage.attemptUpdateText.connect(self.update_text)
