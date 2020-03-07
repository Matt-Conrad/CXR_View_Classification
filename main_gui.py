"""Contains the code for the app that guides the user through the process."""
import logging
import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QProgressBar, QLabel
from main import Controller

logging.basicConfig(filename='CXR_Classification.log', level=logging.INFO)

def run_app():
    """Run application that guides the user through the process."""
    app = QApplication(sys.argv)
    ex = MainApplication()
    sys.exit(app.exec_())

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

        # Variables
        self.controller = Controller()
        
        # Set up GUI
        self.fill_window()
        logging.info('Done constructing Main app')

    def __del__(self):
        """On exit of the Main app close the connection."""
        sys.exit(0)

    def fill_window(self):
        """Displays the content into the window."""
        upper_buttons = QHBoxLayout()
        lower_buttons = QHBoxLayout()
        all_buttons = QVBoxLayout()

        msg_box = QLabel('Welcome to the CXR Classification Application')
        pro_bar = QProgressBar(self)

        self.download_btn = QPushButton('Download', self)
        self.download_btn.clicked.connect(self.controller.download_dataset)
        upper_buttons.addWidget(self.download_btn)

        self.unpack_btn = QPushButton('Unpack', self)
        self.unpack_btn.clicked.connect(self.controller.unpack_dataset)
        upper_buttons.addWidget(self.unpack_btn)

        self.store_btn = QPushButton('Store Metadata', self)
        self.store_btn.clicked.connect(self.controller.store_metadata)
        upper_buttons.addWidget(self.store_btn)

        self.features_btn = QPushButton('Calculate Features', self)
        self.features_btn.clicked.connect(self.controller.calculate_features)
        lower_buttons.addWidget(self.features_btn)

        self.label_btn = QPushButton('Label Images', self)
        self.label_btn.clicked.connect(self.controller.label_images)
        lower_buttons.addWidget(self.label_btn)

        self.classify_btn = QPushButton('Classify Images', self)
        self.classify_btn.clicked.connect(self.controller.classification)
        lower_buttons.addWidget(self.classify_btn)
        
        all_buttons.addWidget(msg_box)
        all_buttons.addWidget(pro_bar)
        all_buttons.addLayout(upper_buttons)
        all_buttons.addLayout(lower_buttons)

        self.setLayout(all_buttons)

        self.init_gui_state()

        self.show()

    def init_gui_state(self):
        if not os.path.exists(self.controller.url):
            self.unpack_btn.setDisabled(True)
            self.store_btn.setDisabled(True)
            self.features_btn.setDisabled(True)
            self.label_btn.setDisabled(True)
            self.classify_btn.setDisabled(True)
    
if __name__ == "__main__":
    run_app()
