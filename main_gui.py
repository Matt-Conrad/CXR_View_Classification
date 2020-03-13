"""Contains the code for the app that guides the user through the process."""
import logging
import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QProgressBar, QLabel

class MainApplication(QWidget):
    """Contains code for the application used guide the user through the process."""
    def __init__(self):
        """App constructor.

        Parameters
        ----------
        QWidget : Class
            Application inherits properties from QWidget
        """
        logging.info('Constructing Main app')
        super().__init__()
        
        # Set up GUI
        self.fill_window()
        logging.info('Done constructing Main app')

    def __del__(self):
        """On exit of the Main app close the connection."""
        sys.exit(0)

    def fill_window(self):
        """Displays the content into the window."""
        self.feedback_dashboard = QVBoxLayout()
        self.msg_box = QLabel('Welcome to the CXR Classification Application')
        self.pro_bar = QProgressBar(self)
        self.feedback_dashboard.addWidget(self.msg_box)
        self.feedback_dashboard.addWidget(self.pro_bar)

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

        self.classify_btn = QPushButton('Classify Images', self)
        lower_buttons.addWidget(self.classify_btn)
        
        all_buttons = QVBoxLayout()
        all_buttons.addLayout(self.feedback_dashboard)
        all_buttons.addLayout(upper_buttons)
        all_buttons.addLayout(lower_buttons)

        self.setLayout(all_buttons)

        self.show()

    def stage1_ui(self):
        self.unpack_btn.setDisabled(True)
        self.store_btn.setDisabled(True)
        self.features_btn.setDisabled(True)
        self.label_btn.setDisabled(True)
        self.classify_btn.setDisabled(True)

    def stage2_ui(self):
        self.download_btn.setDisabled(True)
        self.unpack_btn.setDisabled(False)
        self.store_btn.setDisabled(True)
        self.features_btn.setDisabled(True)
        self.label_btn.setDisabled(True)
        self.classify_btn.setDisabled(True)

    def stage3_ui(self):
        self.download_btn.setDisabled(True)
        self.unpack_btn.setDisabled(True)
        self.store_btn.setDisabled(False)
        self.features_btn.setDisabled(True)
        self.label_btn.setDisabled(True)
        self.classify_btn.setDisabled(True)

    def stage4_ui(self):
        self.download_btn.setDisabled(True)
        self.unpack_btn.setDisabled(True)
        self.store_btn.setDisabled(True)
        self.features_btn.setDisabled(False)
        self.label_btn.setDisabled(True)
        self.classify_btn.setDisabled(True)

    def stage5_ui(self):
        self.download_btn.setDisabled(True)
        self.unpack_btn.setDisabled(True)
        self.store_btn.setDisabled(True)
        self.features_btn.setDisabled(True)
        self.label_btn.setDisabled(False)
        self.classify_btn.setDisabled(True)

    def stage6_ui(self):
        self.download_btn.setDisabled(True)
        self.unpack_btn.setDisabled(True)
        self.store_btn.setDisabled(True)
        self.features_btn.setDisabled(True)
        self.label_btn.setDisabled(True)
        self.classify_btn.setDisabled(False)
