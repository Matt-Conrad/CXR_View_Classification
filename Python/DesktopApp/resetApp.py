from metadata_to_db.databaseHandler import DatabaseHandler
from cxrConfigHandler import CxrConfigHandler
from shutil import rmtree, copyfile
import atexit
import os

class AppResetter:
    def __init__(self):
        configFilename = "config.ini"
        parentFolder = os.path.dirname(os.path.abspath(__file__))
        miscFolderRelPath = os.path.join(os.path.dirname(os.path.dirname(parentFolder)), "miscellaneous")
        configFilePath = os.path.join(parentFolder, configFilename)
        copyfile(os.path.join(miscFolderRelPath, configFilename), configFilePath)
        atexit.register(self.cleanUp)
        
        self.configHandler = CxrConfigHandler(configFilePath)
        self.dbHandler = DatabaseHandler(self.configHandler)

    def cleanUp(self):
        self.deleteFile(self.configHandler.getConfigFilePath())

    def toBeforeStage1(self):
        self.deleteFile(self.configHandler.getTgzFilePath())
        self.deleteUncompressedFolder()
        self.deleteDb()
        self.cleanupTrainOutput()

    def toBeforeStage2(self):
        self.deleteUncompressedFolder()
        self.deleteDb()
        self.cleanupTrainOutput()

    def toBeforeStage3(self):
        self.deleteDb()
        self.cleanupTrainOutput()

    def toBeforeStage4(self):
        self.deleteTable(self.configHandler.getTableName("features"))
        self.deleteTable(self.configHandler.getTableName("label"))
        self.cleanupTrainOutput()

    def toBeforeStage5(self):
        self.deleteTable(self.configHandler.getTableName("label"))
        self.cleanupTrainOutput()

    def toBeforeStage6(self):
        self.cleanupTrainOutput()

    def cleanupTrainOutput(self):
        self.deleteFile(os.path.join(self.configHandler.getParentFolder(), "full_set_classifier.joblib"))
        self.deleteFile(os.path.join(self.configHandler.getParentFolder(), "test_images.csv"))
        
    def deleteFile(self, fileNameOrPath):
        try:
            os.remove(fileNameOrPath)
        except: 
            pass

    def deleteDb(self):
        try:
            self.dbHandler.dropDb(self.configHandler.getDbInfo()['database'])
        except:
            pass

    def deleteTable(self, table_name):
        try:
            self.dbHandler.dropTable(table_name)
        except:
            pass

    def deleteUncompressedFolder(self):
        try:
            rmtree(self.configHandler.getUnpackFolderPath())
        except:
            pass

if __name__ == "__main__":
    resetter = AppResetter()
    resetter.toBeforeStage1()