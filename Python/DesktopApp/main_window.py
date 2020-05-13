"""Contains GUI code for the application."""
import logging
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QProgressBar, QLabel
from buttons import DownloadButton, UnpackButton, StoreButton, CalculateButton, LabelButton, ClassificationButton

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

        self.download_btn = DownloadButton("Download", self, self.controller)
        upper_buttons.addWidget(self.download_btn)

        self.unpack_btn = UnpackButton('Unpack', self, self.controller)
        upper_buttons.addWidget(self.unpack_btn)

        self.store_btn = StoreButton('Store Metadata', self, self.controller)
        upper_buttons.addWidget(self.store_btn)

        self.features_btn = CalculateButton('Calculate Features', self, self.controller)
        lower_buttons.addWidget(self.features_btn)

        self.label_btn = LabelButton('Label Images', self, self.controller)
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

    def update_pro_bar(self, value):
        """Updates the progress bar."""
        self.pro_bar.setValue(value)

    def update_text(self, text):
        """Updates the text."""
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
