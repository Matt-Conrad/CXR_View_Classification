"""Contains the code for the app that guides the user through the process."""
import logging
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
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

        download_btn = QPushButton('Download', self)
        download_btn.clicked.connect(self.download)
        download_btn.move(0, 150)

        unpack_btn = QPushButton('Unpack', self)
        unpack_btn.clicked.connect(self.unpack)
        unpack_btn.move(200, 150)

        store_btn = QPushButton('Store Metadata', self)
        store_btn.clicked.connect(self.store_metadata)
        store_btn.move(400, 150)

        features_btn = QPushButton('Calculate Features', self)
        features_btn.clicked.connect(self.calculate_features)
        features_btn.move(0, 300)

        label_btn = QPushButton('Label Images', self)
        label_btn.clicked.connect(self.label_images)
        label_btn.move(200, 300)

        classify_btn = QPushButton('Classify Images', self)
        classify_btn.clicked.connect(self.classification)
        classify_btn.move(400, 300)

        self.show()

    def download(self):
        """Callback function for the download button."""
        print('Download dummy')
        self.controller.download_dataset()

    def unpack(self):
        """Callback function for the unpack button."""
        self.controller.unpack_dataset()

    def store_metadata(self):
        """Callback function for the store metadata button."""
        self.controller.store_metadata()
    
    def calculate_features(self):
        """Callback function for the calculate_features button."""
        self.controller.calculate_features()
    
    def label_images(self):
        """Callback function for the label_images button."""
        self.controller.label_images()
    
    def classification(self):
        """Callback function for the classification button."""
        self.controller.classification()
    
if __name__ == "__main__":
    run_app()
