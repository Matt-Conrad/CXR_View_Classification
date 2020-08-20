"""Contains GUI code for the application."""
import logging
from PyQt5.QtCore import pyqtSlot, QThread
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QProgressBar, QLabel, QPushButton
from buttons import ClassificationButton
from unpacker import Unpacker, UnpackUpdater

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

        self.classify_btn = ClassificationButton('Train Classifier', self, self.controller)
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
        self.controller.downloader.attemptUpdateProBarBounds.connect(self.update_pro_bar_bounds)
        self.controller.downloader.attemptUpdateProBarValue.connect(self.update_pro_bar_val)
        self.controller.downloader.attemptUpdateText.connect(self.update_text)

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
        self.updater = UnpackUpdater(self.controller.configHandler, self.controller.expected_num_files)

        # Unpacker
        self.unpackThread = QThread()
        self.unpacker.moveToThread(self.unpackThread)
        self.unpack_btn.clicked.connect(self.unpackThread.start)
        self.unpackThread.started.connect(self.unpacker.unpack)

        self.unpacker.finished.connect(self.unpackThread.quit)
        self.unpacker.finished.connect(self.unpacker.deleteLater)
        self.unpackThread.finished.connect(self.unpackThread.deleteLater)

        # Unpack Updater
        self.updaterThread = QThread()
        self.updater.moveToThread(self.updaterThread)
        self.unpack_btn.clicked.connect(self.updaterThread.start)
        self.updaterThread.started.connect(self.updater.update)

        self.updater.attemptUpdateProBarBounds.connect(self.update_pro_bar_bounds)
        self.updater.attemptUpdateProBarValue.connect(self.update_pro_bar_val)
        self.updater.attemptUpdateText.connect(self.update_text)
        
        self.updater.finished.connect(self.stage3_ui)
        self.updater.finished.connect(self.updaterThread.quit)
        self.updater.finished.connect(self.updater.deleteLater)
        self.updaterThread.finished.connect(self.updaterThread.deleteLater)

    @pyqtSlot()
    def stage3_ui(self):
        # User in store metadata phase
        self.download_btn.setDisabled(True)
        self.unpack_btn.setDisabled(True)
        self.store_btn.setDisabled(False)
        self.features_btn.setDisabled(True)
        self.label_btn.setDisabled(True)
        self.classify_btn.setDisabled(True)

        self.store_btn.clicked.connect(self.controller.storer.dicomToDb)

        self.controller.storer.attemptUpdateProBarBounds.connect(self.update_pro_bar_bounds)
        self.controller.storer.attemptUpdateProBarValue.connect(self.update_pro_bar_val)
        self.controller.storer.attemptUpdateText.connect(self.update_text)

        self.controller.storer.finished.connect(self.stage4_ui)
        self.controller.storer.finished.connect(self.controller.storer.deleteLater)

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

        self.controller.featCalc.attemptUpdateProBarBounds.connect(self.update_pro_bar_bounds)
        self.controller.featCalc.attemptUpdateProBarValue.connect(self.update_pro_bar_val)
        self.controller.featCalc.attemptUpdateText.connect(self.update_text)

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

        self.label_btn.clicked.connect(self.controller.labeler.label_images)

        self.controller.labeler.attemptUpdateProBarBounds.connect(self.update_pro_bar_bounds)
        self.controller.labeler.attemptUpdateProBarValue.connect(self.update_pro_bar_val)
        self.controller.labeler.attemptUpdateText.connect(self.update_text)

        self.controller.labeler.finished.connect(self.stage6_ui)
        self.controller.labeler.finished.connect(self.controller.labeler.deleteLater)

    @pyqtSlot()
    def stage6_ui(self):
        # User in classification phase
        self.download_btn.setDisabled(True)
        self.unpack_btn.setDisabled(True)
        self.store_btn.setDisabled(True)
        self.features_btn.setDisabled(True)
        self.label_btn.setDisabled(True)
        self.classify_btn.setDisabled(False)
