import logging
from PyQt5.QtCore import QObject
from downloadStage import DownloadStage
from unpackStage import UnpackStage
from storeStage import StoreStage
from featureCalculatorStage import FeatCalcStage
from labelStage import LabelStage
from trainStage import TrainStage
from cxrConfigHandler import CxrConfigHandler
from metadata_to_db.database_handler import DatabaseHandler
from mainWindow import MainWindow

class Controller(QObject):
    """Controller class that controls the logic of the application."""
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

        logging.info('***CONTROLLER INITIALIZED***')

    def configureLogging(self):
        # Get log level from config file
        logLevel = self.configHandler.getSetting(sectionName='logging', settingName='level')
        if logLevel == 'debug':
            logLevelObj = logging.DEBUG
        elif logLevel == 'info':
            logLevelObj = logging.INFO
        
        # Remove any log handlers to make way for our logger
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        
        # Set the logging
        logging.basicConfig(filename='CXR_Classification.log', level=logLevelObj,
                            format='%(asctime)s %(levelname)-8s: %(message)s', datefmt='%Y-%m-%d|%H:%M:%S')
