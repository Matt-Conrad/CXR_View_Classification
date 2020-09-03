import logging
import os
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QIcon
from downloader import Downloader
from labeler import Labeler
from label_importer import LabelImporter
from trainer import Trainer
from feature_calculator import FeatureCalculator
from cxr_config_handler import CxrConfigHandler
from metadata_to_db.database_handler import DatabaseHandler
from main_window import MainWindow

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
        self.configHandler = CxrConfigHandler("./config.ini")
        self.configureLogging()

        logging.info('***INITIALIZING CONTROLLER***')
        QObject.__init__(self)

        self.dbHandler = DatabaseHandler(self.configHandler)

        self.downloader = Downloader(self.configHandler)
        self.featCalc = FeatureCalculator(self.configHandler, self.dbHandler)
        self.labeler = Labeler(self.configHandler, self.dbHandler)
        self.label_importer = LabelImporter(self.configHandler, self.dbHandler)
        self.trainer = Trainer(self.configHandler, self.dbHandler)

        self.main_app = MainWindow(self)

        self.init_gui_state()
        logging.info('***CONTROLLER INITIALIZED***')

    def init_gui_state(self):
        self.main_app.setWindowIcon(QIcon(self.configHandler.getParentFolder() + '/' + 'icon.jpg'))

        self.initStage1.connect(self.main_app.stage1_ui)
        self.initStage2.connect(self.main_app.stage2_ui)
        self.initStage3.connect(self.main_app.stage3_ui)
        self.initStage4.connect(self.main_app.stage4_ui)
        self.initStage5.connect(self.main_app.stage5_ui)
        self.initStage6.connect(self.main_app.stage6_ui)

        # Initialize in right stage
        if self.dbHandler.table_exists(self.configHandler.getTableName("label")):
            self.initStage6.emit()
        elif self.dbHandler.table_exists(self.configHandler.getTableName("features")):
            self.initStage5.emit()
        elif self.dbHandler.table_exists(self.configHandler.getTableName("metadata")):
            self.initStage4.emit()
        elif os.path.isdir(self.configHandler.getDatasetName()):
            self.initStage3.emit()
        elif os.path.exists(self.configHandler.getTgzFilename()):
            self.initStage2.emit()
        else:
            self.initStage1.emit()

    def configureLogging(self):
        # Get log level from config file
        log_level = self.configHandler.getSetting(sectionName='logging', settingName='level')
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
