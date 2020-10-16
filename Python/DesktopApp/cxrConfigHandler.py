from PyQt5.QtCore import pyqtSlot
from metadata_to_db.configHandler import ConfigHandler
from expectedSizes import SOURCE_URL
import os

class CxrConfigHandler(ConfigHandler):
    """Config handler specifically for CXR project."""
    def __init__(self, configFilePath):
        ConfigHandler.__init__(self, configFilePath)
        self.prepConfigIni()

    def prepConfigIni(self):
        self.setUrl(SOURCE_URL[self.getDatasetType()])
        self.setParentFolder()
        self.setCsvPath()
        self.setColumnsInfoName()

    # Getters 
    def getUrl(self):
        return self.getSetting("misc", "url")

    def getParentFolder(self):
        return self.getSetting('misc', "parent_folder")

    def getCsvPath(self):
        return self.getSetting("misc","csv_relative_path")

    def getColumnsInfoName(self):
        return self.getSetting("misc", 'columns_info_name')

    def getColumnsInfoFullPath(self):
        return os.path.join(self.getParentFolder(), self.getColumnsInfoName())

    def getDbInfo(self):
        return self.getSection('postgresql')

    def getTableName(self, table):
        return self.getSetting('table_names', table)

    def getTgzFilename(self):
        return self.getUrl().split("/")[-1]
    
    def getTgzFilePath(self):
        return os.path.join(self.getParentFolder(), self.getTgzFilename()) 

    def getDatasetName(self):
        return self.getTgzFilename().split(".")[0]

    def getUnpackFolderPath(self):
        return os.path.join(self.getParentFolder(), self.getDatasetName())

    def getDatasetType(self):
        return self.getSetting("dataset_info", "dataset")

    def getLogLevel(self):
        return self.getSetting("logging", "level")

    # Setters
    def setUrl(self, url):
        self.setSetting("misc", "url", url)

    def setParentFolder(self):
        self.setSetting("misc", "parent_folder", os.path.dirname(self.getConfigFilePath()))

    def setCsvPath(self):
        self.setSetting("misc", "csv_relative_path", "./image_labels.csv")

    def setColumnsInfoName(self):
        self.setSetting("misc", "columns_info_name", "columns_info.json")