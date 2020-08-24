import metadata_to_db.config as config
from os.path import dirname, abspath
from expected_sizes import SOURCE_URL

class ConfigHandler:
    """Contains GUI code for the application."""
    def __init__(self, configFilename):
        self.configFilename = configFilename
        self.prepConfigIni()

    def prepConfigIni(self):
        self.setUrl(SOURCE_URL[self.getDatasetType()])
        self.setParentFolder()
        self.setCsvPath()
        self.setColumnsInfoPath()

    # Functions for internal use
    def getSection(self, sectionName):
        return config.config(filename=self.configFilename, section=sectionName)
    
    def getSetting(self, sectionName, settingName):
        return config.config(filename=self.configFilename, section=sectionName)[settingName]

    def setSetting(self, sectionName, settingName, value):
        config.update_config_file(self.configFilename, sectionName, settingName, value)

    # Functions for external use
    def getUrl(self):
        return self.getSetting("misc", "url")

    def setUrl(self, url):
        self.setSetting("misc", "url", url)

    def getParentFolder(self):
        return self.getSetting('misc', "parent_folder")

    def setParentFolder(self):
        self.setSetting("misc", "parent_folder", dirname(abspath(__file__)))

    def getCsvPath(self):
        return self.getSetting("misc","csv_relative_path")

    def setCsvPath(self):
        self.setSetting("misc", "csv_relative_path", "./image_labels.csv")

    def getColumnsInfoPath(self):
        return self.getSetting("misc", 'columns_info_relative_path')

    def setColumnsInfoPath(self):
        self.setSetting("misc", "columns_info_relative_path", "./columns_info.json")

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

    def getConfigFilename(self):
        return self.configFilename