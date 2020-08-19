import metadata_to_db.config as config

class ConfigHandler:
    """Contains GUI code for the application."""
    def __init__(self, configFilename):
        self.configFilename = configFilename

    def setUrl(self, url):
        config.update_config_file(self.configFilename, "misc", "url", url)

    def getDbInfo(self):
        return config.config(filename=self.configFilename, section='postgresql')

    def getTableName(self, table):
        return config.config(filename=self.configFilename, section='table_names')[table]

    def getUrl(self):
        return config.config(filename=self.configFilename, section='misc')['url']

    def getTgzFilename(self):
        return self.getUrl().split("/")[-1]

    def getDatasetName(self):
        return self.getTgzFilename().split(".")[0]

    def getColumnsInfoPath(self):
        return config.config(filename=self.configFilename, section='misc')['columns_info_relative_path']

    def getCsvPath(self):
        return config.config(filename=self.configFilename, section='misc')['csv_relative_path']

    def getDatasetType(self):
        return config.config(filename=self.configFilename, section='dataset_info')['dataset']

    def getParentFolder(self):
        return config.config(filename=self.configFilename, section='misc')['parent_folder']