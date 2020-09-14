from PyQt5.QtCore import pyqtSlot
from metadata_to_db.config_handler import ConfigHandler
from expectedSizes import SOURCE_URL
import os

class CxrConfigHandler(ConfigHandler):
    """Config handler specifically for CXR project."""
    def __init__(self, configFilename):
        ConfigHandler.__init__(self, configFilename)
        self.prepConfigIni()

    def prepConfigIni(self):
        self.setUrl(SOURCE_URL[self.getDatasetType()])
        self.setParentFolder()
        self.setCsvPath()
        self.setColumnsInfoPath()

    # Getters 
    def getUrl(self):
        return self.getSetting("misc", "url")

    def getParentFolder(self):
        return self.getSetting('misc', "parent_folder")

    def getCsvPath(self):
        return self.getSetting("misc","csv_relative_path")

    def getColumnsInfoPath(self):
        return self.getSetting("misc", 'columns_info_relative_path')

    def getDbInfo(self):
        return self.getSection('postgresql')

    def getTableName(self, table):
        return self.getSetting('table_names', table)

    def getTgzFilename(self):
        return self.getUrl().split("/")[-1]

    def getDatasetName(self):
        return self.getTgzFilename().split(".")[0]

    def getDatasetType(self):
        return self.getSetting("dataset_info", "dataset")

    # Setters
    def setUrl(self, url):
        self.setSetting("misc", "url", url)

    def setParentFolder(self):
        self.setSetting("misc", "parent_folder", os.getcwd())

    def setCsvPath(self):
        self.setSetting("misc", "csv_relative_path", "./image_labels.csv")

    def setColumnsInfoPath(self):
        self.setSetting("misc", "columns_info_relative_path", "./columns_info.json")