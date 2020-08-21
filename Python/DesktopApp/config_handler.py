import metadata_to_db.config as config

class ConfigHandler:
    """Contains GUI code for the application."""
    def __init__(self, configFilename):
        self.configFilename = configFilename

    # Functions for internal use
    def getSection(self, sectionName):
        return config.config(filename=self.configFilename, section=sectionName)
    
    def getSetting(self, sectionName, settingName):
        return config.config(filename=self.configFilename, section=sectionName)[settingName]

    def setSetting(self, sectionName, settingName, value):
        config.update_config_file(self.configFilename, sectionName, settingName, value)

    # Functions for external use
    def setUrl(self, url):
        self.setSetting("misc", "url", url)

    def getDbInfo(self):
        return self.getSection('postgresql')

    def getTableName(self, table):
        return self.getSetting('table_names', table)

    def getUrl(self):
        return self.getSetting("misc", "url")

    def getTgzFilename(self):
        return self.getUrl().split("/")[-1]

    def getDatasetName(self):
        return self.getTgzFilename().split(".")[0]

    def getColumnsInfoPath(self):
        return self.getSetting("misc", 'columns_info_relative_path')

    def getCsvPath(self):
        return self.getSetting("misc","csv_relative_path")

    def getDatasetType(self):
        return self.getSetting("dataset_info", "dataset")

    def getParentFolder(self):
        return self.getSetting('misc', "parent_folder")

    def getConfigFilename(self):
        return self.configFilename