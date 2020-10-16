import pytest
from pytest_postgresql import factories
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cxrConfigHandler import CxrConfigHandler
from metadata_to_db.databaseHandler import DatabaseHandler
from downloadStage import DownloadStage
from unpackStage import UnpackStage
from storeStage import StoreStage
from featureCalculatorStage import FeatCalcStage
from labelStage import LabelStage
from trainStage import TrainStage
import shutil


configFilename = "config.ini"
tgzFilename = "NLMCXR_subset_dataset.tgz"
dcmFolderName = tgzFilename.split(".")[0]
columnsInfoFilename = "columns_info.json"
csvFilename = "image_labels.csv"
imageMetadataBackupFilename = "image_metadata.sql"
featuresBackupFilename = "features.sql"
imageLabelsBackupFilename = "image_labels.sql"
testDataRelPath = "./testData"

configRelPath = os.path.join(testDataRelPath, configFilename)
tgzRelPath = os.path.join(testDataRelPath, tgzFilename)
dcmFolderRelPath = os.path.join(testDataRelPath, dcmFolderName)
columnsInfoRelPath = os.path.join(testDataRelPath, columnsInfoFilename)
csvRelPath = os.path.join(testDataRelPath, csvFilename)
imageMetadataBackupRelPath = os.path.join(testDataRelPath, imageMetadataBackupFilename)
featuresBackupRelPath = os.path.join(testDataRelPath, featuresBackupFilename)
imageLabelsBackupRelPath = os.path.join(testDataRelPath, imageLabelsBackupFilename)

postgresql_my_proc = factories.postgresql_noproc(host="127.0.0.1", port=5432, user="postgres", password="postgres")
postgresql_my = factories.postgresql('postgresql_my_proc', db_name="testDb")

@pytest.fixture(scope="class")
def cxrConfigHandler(tmpdir_factory):
    direct = tmpdir_factory.mktemp("cxrConfigHandler")
    testConfigFullPath = os.path.join(str(direct), configFilename)
    shutil.copyfile(configRelPath, testConfigFullPath)
    return CxrConfigHandler(testConfigFullPath)

@pytest.fixture(scope="function")
def databaseHandler(tmpdir_factory, postgresql_my): # Creates a new database for each test function
    pgtest = postgresql_my
    direct = tmpdir_factory.mktemp("databaseHandler")
    testConfigFullPath = os.path.join(str(direct), configFilename)
    shutil.copyfile(configRelPath, testConfigFullPath)
    configHandler = CxrConfigHandler(testConfigFullPath)
    return DatabaseHandler(configHandler)

@pytest.fixture(scope="class")
def downloadStage(tmpdir_factory):
    direct = tmpdir_factory.mktemp("downloadStage")
    testConfigFullPath = os.path.join(str(direct), configFilename)
    shutil.copyfile(configRelPath, testConfigFullPath)
    configHandler = CxrConfigHandler(testConfigFullPath)
    return DownloadStage(configHandler)

@pytest.fixture(scope="class")
def unpackStage(tmpdir_factory):
    direct = tmpdir_factory.mktemp("unpackStage")
    testConfigFullPath = os.path.join(str(direct), configFilename)
    shutil.copyfile(configRelPath, testConfigFullPath)
    configHandler = CxrConfigHandler(testConfigFullPath)
    shutil.copyfile(tgzRelPath, configHandler.getTgzFilePath())
    return UnpackStage(configHandler)

@pytest.fixture(scope="function")
def storeStage(tmpdir_factory, postgresql_my):
    pgtest = postgresql_my
    direct = tmpdir_factory.mktemp("storeStage")
    testConfigFullPath = os.path.join(str(direct), configFilename)
    shutil.copyfile(configRelPath, testConfigFullPath)
    configHandler = CxrConfigHandler(testConfigFullPath)

    shutil.copyfile(columnsInfoRelPath, configHandler.getColumnsInfoFullPath())
    shutil.copytree(dcmFolderRelPath, configHandler.getUnpackFolderPath())
    
    dbHandler = DatabaseHandler(configHandler)
    return StoreStage(configHandler, dbHandler)

@pytest.fixture(scope="function")
def featCalcStage(tmpdir_factory, postgresql_my):
    pgtest = postgresql_my

    direct = tmpdir_factory.mktemp("featCalcStage")
    testConfigFullPath = os.path.join(str(direct), configFilename)
    shutil.copyfile(configRelPath, testConfigFullPath)
    configHandler = CxrConfigHandler(testConfigFullPath)

    shutil.copyfile(columnsInfoRelPath, configHandler.getColumnsInfoFullPath())
    shutil.copytree(dcmFolderRelPath, configHandler.getUnpackFolderPath())
    
    dbHandler = DatabaseHandler(configHandler)
    dbHandler.executeQuery(dbHandler.connection, open(imageMetadataBackupRelPath, "r").read())

    return FeatCalcStage(configHandler, dbHandler)

@pytest.fixture(scope="function")
def manualLabelStage(tmpdir_factory, postgresql_my):
    pgtest = postgresql_my

    direct = tmpdir_factory.mktemp("manualLabelStage")

    testConfigFullPath = os.path.join(str(direct), configFilename)
    shutil.copyfile(configRelPath, testConfigFullPath)
    configHandler = CxrConfigHandler(testConfigFullPath)

    shutil.copyfile(columnsInfoRelPath, configHandler.getColumnsInfoFullPath())

    dbHandler = DatabaseHandler(configHandler)
    dbHandler.executeQuery(dbHandler.connection, open(imageMetadataBackupRelPath, "r").read())
    dbHandler.executeQuery(dbHandler.connection, open(featuresBackupRelPath, "r").read())
    return LabelStage(configHandler, dbHandler)

@pytest.fixture(scope="function")
def importLabelStage(tmpdir_factory, postgresql_my):
    pgtest = postgresql_my

    direct = tmpdir_factory.mktemp("importLabelStage")

    testConfigFullPath = os.path.join(str(direct), configFilename)
    shutil.copyfile(configRelPath, testConfigFullPath)
    configHandler = CxrConfigHandler(testConfigFullPath)

    shutil.copyfile(columnsInfoRelPath, configHandler.getColumnsInfoFullPath())
    shutil.copyfile(csvRelPath, configHandler.getCsvPath())

    dbHandler = DatabaseHandler(configHandler)  
    configHandler.setSetting("dataset_info", "dataset", "full_set")
    return LabelStage(configHandler, dbHandler)

@pytest.fixture(scope="function")
def trainStage(tmpdir_factory, postgresql_my):
    pgtest = postgresql_my

    direct = tmpdir_factory.mktemp("trainStage")

    testConfigFullPath = os.path.join(str(direct), configFilename)
    shutil.copyfile(configRelPath, testConfigFullPath)
    configHandler = CxrConfigHandler(testConfigFullPath)
    dbHandler = DatabaseHandler(configHandler)

    dbHandler.executeQuery(dbHandler.connection, open(featuresBackupRelPath, "r").read())
    dbHandler.executeQuery(dbHandler.connection, open(imageLabelsBackupRelPath, "r").read())

    return TrainStage(configHandler, dbHandler)