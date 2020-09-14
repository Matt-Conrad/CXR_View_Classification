import logging
import os
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QIcon
from downloadStage import DownloadStage
from unpackStage import UnpackStage
from storeStage import StoreStage
from featureCalculatorStage import FeatCalcStage
from labelStage import LabelStage
from trainStage import TrainStage
from cxr_config_handler import CxrConfigHandler
from metadata_to_db.database_handler import DatabaseHandler
from main_window import MainWindow

class Controller(QObject):
    """Controller class that controls the logic of the application."""
    # Signals
    initDownloadStage = pyqtSignal()
    initUnpackStage = pyqtSignal()
    initStoreStage = pyqtSignal()
    initCalcFeatStage = pyqtSignal()
    initLabelStage = pyqtSignal()
    initTrainStage = pyqtSignal()

    def __init__(self):
        self.configHandler = CxrConfigHandler("./config.ini")
        self.configureLogging()

        logging.info('***INITIALIZING CONTROLLER***')
        QObject.__init__(self)

        self.dbHandler = DatabaseHandler(self.configHandler)

        self.downloadStage = DownloadStage(self.configHandler)
        self.unpackStage = UnpackStage(self.configHandler)
        self.storeStage = StoreStage(self.configHandler, self.dbHandler)
        self.featCalcStage = FeatCalcStage(self.configHandler, self.dbHandler)
        self.labelStage = LabelStage(self.configHandler, self.dbHandler)
        self.trainStage = TrainStage(self.configHandler, self.dbHandler)

        self.mainWindow = MainWindow(self)

        self.initGuiState()
        logging.info('***CONTROLLER INITIALIZED***')

    def initGuiState(self):
        self.mainWindow.setWindowIcon(QIcon(self.configHandler.getParentFolder() + '/' + 'icon.jpg'))

        self.initDownloadStage.connect(self.mainWindow.downloadStageUi)
        self.initUnpackStage.connect(self.mainWindow.unpackStageUi)
        self.initStoreStage.connect(self.mainWindow.storeStageUi)
        self.initCalcFeatStage.connect(self.mainWindow.calcFeatStageUi)
        self.initLabelStage.connect(self.mainWindow.labelStageUi)
        self.initTrainStage.connect(self.mainWindow.trainStageUi)

        # Initialize in right stage
        if self.dbHandler.table_exists(self.configHandler.getTableName("label")):
            self.initTrainStage.emit()
        elif self.dbHandler.table_exists(self.configHandler.getTableName("features")):
            self.initLabelStage.emit()
        elif self.dbHandler.table_exists(self.configHandler.getTableName("metadata")):
            self.initCalcFeatStage.emit()
        elif os.path.isdir(self.configHandler.getDatasetName()):
            self.initStoreStage.emit()
        elif os.path.exists(self.configHandler.getTgzFilename()):
            self.initUnpackStage.emit()
        else:
            self.initDownloadStage.emit()

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
