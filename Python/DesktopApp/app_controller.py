"""Contains the software coordinating the logic of the application."""
import logging
import os
import sys
from PyQt5.QtCore import QThreadPool, QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from downloader import Downloader
from storer import Storer
from labeler import Labeler
from trainer import Trainer
from feature_calculator import FeatureCalculator
from config_handler import ConfigHandler
from database_handler import DatabaseHandler
import metadata_to_db.basic_db_ops as bdo
import metadata_to_db.config as config
from main_window import MainWindow
from expected_sizes import EXPECTED_NUM_FILES, EXPECTED_SIZES

SOURCE_URL = {
        'subset': 'https://github.com/Matt-Conrad/CXR_View_Classification/raw/develop/datasets/NLMCXR_subset_dataset.tgz',
        'full_set': 'https://openi.nlm.nih.gov/imgs/collections/NLMCXR_dcm.tgz'
    }

CONFIG_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')

def run_app():
    """Run the application that guides the user through the process."""
    app = QApplication(sys.argv)
    cont = Controller()
    app.exec_()

class Controller(QObject):
    """Controller class that controls the logic of the application."""
    # Signals
    initStage1 = pyqtSignal()
    initStage2 = pyqtSignal()
    initStage3 = pyqtSignal()
    initStage4 = pyqtSignal()
    initStage5 = pyqtSignal()
    initStage6 = pyqtSignal()

    def __init__(self):
        logging.info('***INITIALIZING CONTROLLER***')
        QObject.__init__(self)

        self.configHandler = ConfigHandler("./config.ini")
        self.dbHandler = DatabaseHandler(self.configHandler)

        self.downloader = Downloader(self.configHandler)
        self.storer = Storer(self.configHandler, self.dbHandler)
        self.featCalc = FeatureCalculator(self.configHandler, self.dbHandler)
        self.labeler = Labeler(self.configHandler, self.dbHandler)
        self.trainer = Trainer(self.configHandler, self.dbHandler)

        # Object variables
        self.main_app = MainWindow(self)

        # Set up the GUI
        self.init_gui_state()
        logging.info('***CONTROLLER INITIALIZED***')

    ### GUI HELPER FUNCTIONS
    def init_gui_state(self):
        """Initialize the GUI in the right stage."""
        # Set icon
        self.main_app.setWindowIcon(QIcon(self.configHandler.getParentFolder() + '/' + 'icon.jpg'))

        self.initStage1.connect(self.main_app.stage1_ui)
        self.initStage2.connect(self.main_app.stage2_ui)
        self.initStage3.connect(self.main_app.stage3_ui)
        self.initStage4.connect(self.main_app.stage4_ui)
        self.initStage5.connect(self.main_app.stage5_ui)
        self.initStage6.connect(self.main_app.stage6_ui)

        if bdo.table_exists(self.configHandler.getConfigFilename(), self.configHandler.getDbInfo()["database"], self.configHandler.getTableName("label")):
            self.initStage6.emit()
        elif bdo.table_exists(self.configHandler.getConfigFilename(), self.configHandler.getDbInfo()["database"], self.configHandler.getTableName("features")):
            self.initStage5.emit()
        elif bdo.table_exists(self.configHandler.getConfigFilename(), self.configHandler.getDbInfo()["database"], self.configHandler.getTableName("metadata")):
            self.initStage4.emit()
        elif os.path.isdir(self.configHandler.getDatasetName()):
            self.initStage3.emit()
        elif os.path.exists(self.configHandler.getTgzFilename()):
            self.initStage2.emit()
        else:
            self.initStage1.emit()

    def log_gui_state(self, debug_level):
        """Log the state of the feedback in the GUI."""
        if debug_level == 'debug':
            logging.debug('Text: ' + self.main_app.msg_box.text())
            logging.debug('Progress bar value: ' + str(self.main_app.pro_bar.value()))

if __name__ == "__main__":
    # Get log level from config file
    log_level = config.config(filename=CONFIG_NAME, section='logging')['level']
    if log_level == 'debug':
        log_level_obj = logging.DEBUG
    elif log_level == 'info':
        log_level_obj = logging.INFO
    
    # Remove any log handlers to make way for our logger
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    
    # Set the logging
    logging.basicConfig(filename='CXR_Classification.log', level=log_level_obj,
                        format='%(asctime)s %(levelname)-8s: %(message)s', datefmt='%Y-%m-%d|%H:%M:%S')

    # Run the application
    run_app()
