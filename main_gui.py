"""Contains GUI code for the application."""
import logging
import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QProgressBar, QLabel
from PyQt5.QtCore import pyqtSlot

class MainApplication(QWidget):
    """Contains GUI code for the application."""
    def __init__(self):
        logging.info('Constructing Main app')
        super().__init__()
        
        # Set up GUI
        self.fill_window()
        logging.info('Done constructing Main app')

    def fill_window(self):
        """Fills the window with buttons."""
        # "Feedback dashboard" displays progress to the user
        self.feedback_dashboard = QVBoxLayout()
        self.msg_box = QLabel('Welcome to the CXR Classification Application')
        self.pro_bar = QProgressBar(self)
        self.feedback_dashboard.addWidget(self.msg_box)
        self.feedback_dashboard.addWidget(self.pro_bar)

        # Button array
        upper_buttons = QHBoxLayout()
        lower_buttons = QHBoxLayout()

        self.download_btn = QPushButton('Download', self)
        upper_buttons.addWidget(self.download_btn)

        self.unpack_btn = QPushButton('Unpack', self)
        upper_buttons.addWidget(self.unpack_btn)

        self.store_btn = QPushButton('Store Metadata', self)
        upper_buttons.addWidget(self.store_btn)

        self.features_btn = QPushButton('Calculate Features', self)
        lower_buttons.addWidget(self.features_btn)

        self.label_btn = QPushButton('Label Images', self)
        lower_buttons.addWidget(self.label_btn)

        self.classify_btn = QPushButton('Train Classifier', self)
        lower_buttons.addWidget(self.classify_btn)
        
        # Stack the feedback dashboard over the button array
        full_layout = QVBoxLayout()
        full_layout.addLayout(self.feedback_dashboard)
        full_layout.addLayout(upper_buttons)
        full_layout.addLayout(lower_buttons)

        self.setLayout(full_layout)

        self.show()

    def update_pro_bar(self, value):
        self.pro_bar.setValue(value)

    def update_text(self, text):
        self.msg_box.setText(text)

    def stage1_ui(self):
        # User in download phase
        self.download_btn.setDisabled(False)
        self.unpack_btn.setDisabled(True)
        self.store_btn.setDisabled(True)
        self.features_btn.setDisabled(True)
        self.label_btn.setDisabled(True)
        self.classify_btn.setDisabled(True)

    def stage2_ui(self):
        # User in unpack phase
        self.download_btn.setDisabled(True)
        self.unpack_btn.setDisabled(False)
        self.store_btn.setDisabled(True)
        self.features_btn.setDisabled(True)
        self.label_btn.setDisabled(True)
        self.classify_btn.setDisabled(True)

    def stage3_ui(self):
        # User in store metadata phase
        self.download_btn.setDisabled(True)
        self.unpack_btn.setDisabled(True)
        self.store_btn.setDisabled(False)
        self.features_btn.setDisabled(True)
        self.label_btn.setDisabled(True)
        self.classify_btn.setDisabled(True)

    def stage4_ui(self):
        # User in calculate features phase
        self.download_btn.setDisabled(True)
        self.unpack_btn.setDisabled(True)
        self.store_btn.setDisabled(True)
        self.features_btn.setDisabled(False)
        self.label_btn.setDisabled(True)
        self.classify_btn.setDisabled(True)

    def stage5_ui(self):
        # User in labeling phase
        self.download_btn.setDisabled(True)
        self.unpack_btn.setDisabled(True)
        self.store_btn.setDisabled(True)
        self.features_btn.setDisabled(True)
        self.label_btn.setDisabled(False)
        self.classify_btn.setDisabled(True)

    def stage6_ui(self):
        # User in classification phase
        self.download_btn.setDisabled(True)
        self.unpack_btn.setDisabled(True)
        self.store_btn.setDisabled(True)
        self.features_btn.setDisabled(True)
        self.label_btn.setDisabled(True)
        self.classify_btn.setDisabled(False)
