import pytest
from pytest_postgresql import factories
import psycopg2
import psycopg2.extras
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
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

configRelPath = testDataRelPath + os.path.sep + configFilename
tgzRelPath = testDataRelPath + os.path.sep + tgzFilename
dcmFolderRelPath = testDataRelPath + os.path.sep + dcmFolderName
columnsInfoRelPath = testDataRelPath + os.path.sep + columnsInfoFilename
csvRelPath = testDataRelPath + os.path.sep + csvFilename
imageMetadataBackupRelPath = testDataRelPath + os.path.sep + imageMetadataBackupFilename
featuresBackupRelPath = testDataRelPath + os.path.sep + featuresBackupFilename
imageLabelsBackupRelPath = testDataRelPath + os.path.sep + imageLabelsBackupFilename

homePath = os.getcwd()

postgresql_my_proc = factories.postgresql_noproc(host="127.0.0.1", port=5432, user="postgres", password="postgres")
postgresql_my = factories.postgresql('postgresql_my_proc', db_name="testDb")

@pytest.fixture(scope="class")
def cxrConfigHandler(tmpdir_factory):
    os.chdir(homePath)
    direct = tmpdir_factory.mktemp("cxrConfigHandler")
    directPath = str(direct)
    testConfigFullPath = directPath + os.path.sep + configFilename
    shutil.copyfile(configRelPath, testConfigFullPath)
    os.chdir(str(directPath))
    return CxrConfigHandler(testConfigFullPath)

@pytest.fixture(scope="function")
def databaseHandler(tmpdir_factory, postgresql_my): # Creates a new database for each test function
    pgtest = postgresql_my
    os.chdir(homePath)
    direct = tmpdir_factory.mktemp("databaseHandler")
    directPath = str(direct)
    testConfigFullPath = directPath + os.path.sep + configFilename
    shutil.copyfile(configRelPath, testConfigFullPath)
    os.chdir(str(directPath))
    configHandler = CxrConfigHandler(testConfigFullPath)
    return DatabaseHandler(configHandler)

@pytest.fixture(scope="class")
def downloadStage(tmpdir_factory):
    os.chdir(homePath)
    direct = tmpdir_factory.mktemp("downloadStage")
    directPath = str(direct)
    testConfigFullPath = directPath + os.path.sep + configFilename
    shutil.copyfile(configRelPath, testConfigFullPath)
    os.chdir(str(directPath))
    configHandler = CxrConfigHandler(testConfigFullPath)
    return DownloadStage(configHandler)

@pytest.fixture(scope="class")
def unpackStage(tmpdir_factory):
    os.chdir(homePath)
    direct = tmpdir_factory.mktemp("unpackStage")
    directPath = str(direct)
    testConfigFullPath = directPath + os.path.sep + configFilename
    shutil.copyfile(configRelPath, testConfigFullPath)
    shutil.copyfile(tgzRelPath, directPath + os.path.sep + tgzFilename)
    os.chdir(directPath)
    configHandler = CxrConfigHandler(testConfigFullPath)
    return UnpackStage(configHandler)

@pytest.fixture(scope="function")
def storeStage(tmpdir_factory, postgresql_my):
    pgtest = postgresql_my
    os.chdir(homePath)
    direct = tmpdir_factory.mktemp("storeStage")
    directPath = str(direct)
    testConfigFullPath = directPath + os.path.sep + configFilename
    testColumnsInfoFullPath = directPath + os.path.sep + columnsInfoFilename
    testDcmFolderFullPath = directPath + os.path.sep + dcmFolderName
    shutil.copyfile(configRelPath, testConfigFullPath)
    shutil.copyfile(columnsInfoRelPath, testColumnsInfoFullPath)
    shutil.copytree(dcmFolderRelPath, testDcmFolderFullPath)
    os.chdir(directPath)
    configHandler = CxrConfigHandler(testConfigFullPath)
    dbHandler = DatabaseHandler(configHandler)
    return StoreStage(configHandler, dbHandler)

@pytest.fixture(scope="function")
def featCalcStage(tmpdir_factory, postgresql_my):
    pgtest = postgresql_my
    os.chdir(homePath)

    params = {
        "host": "127.0.0.1",
        "port": 5432,
        "database": "testDb",
        "user": "postgres",
        "password": "postgres"
    }
    connection = psycopg2.connect(**params)
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(open(imageMetadataBackupRelPath, "r").read())

    direct = tmpdir_factory.mktemp("featCalcStage")
    directPath = str(direct)
    testConfigFullPath = directPath + os.path.sep + configFilename
    testColumnsInfoFullPath = directPath + os.path.sep + columnsInfoFilename
    testDcmFolderFullPath = directPath + os.path.sep + dcmFolderName
    shutil.copyfile(configRelPath, testConfigFullPath)
    shutil.copyfile(columnsInfoRelPath, testColumnsInfoFullPath)
    shutil.copytree(dcmFolderRelPath, testDcmFolderFullPath)
    os.chdir(directPath)
    configHandler = CxrConfigHandler(testConfigFullPath)
    dbHandler = DatabaseHandler(configHandler)

    return FeatCalcStage(configHandler, dbHandler)

@pytest.fixture(scope="function")
def manualLabelStage(tmpdir_factory, postgresql_my):
    pgtest = postgresql_my
    os.chdir(homePath)

    params = {
        "host": "127.0.0.1",
        "port": 5432,
        "database": "testDb",
        "user": "postgres",
        "password": "postgres"
    }
    connection = psycopg2.connect(**params)
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(open(imageMetadataBackupRelPath, "r").read())
    cursor.execute(open(featuresBackupRelPath, "r").read())

    direct = tmpdir_factory.mktemp("manualLabelStage")
    directPath = str(direct)
    testConfigFullPath = directPath + os.path.sep + configFilename
    testColumnsInfoFullPath = directPath + os.path.sep + columnsInfoFilename
    shutil.copyfile(configRelPath, testConfigFullPath)
    shutil.copyfile(columnsInfoRelPath, testColumnsInfoFullPath)
    os.chdir(directPath)
    configHandler = CxrConfigHandler(testConfigFullPath)
    dbHandler = DatabaseHandler(configHandler)
    return LabelStage(configHandler, dbHandler)

@pytest.fixture(scope="function")
def importLabelStage(tmpdir_factory, postgresql_my):
    pgtest = postgresql_my
    os.chdir(homePath)

    direct = tmpdir_factory.mktemp("importLabelStage")
    directPath = str(direct)
    testConfigFullPath = directPath + os.path.sep + configFilename
    testColumnsInfoFullPath = directPath + os.path.sep + columnsInfoFilename
    testCsvFullPath = directPath + os.path.sep + csvFilename
    shutil.copyfile(configRelPath, testConfigFullPath)
    shutil.copyfile(columnsInfoRelPath, testColumnsInfoFullPath)
    shutil.copyfile(csvRelPath, testCsvFullPath)
    os.chdir(directPath)
    configHandler = CxrConfigHandler(testConfigFullPath)
    configHandler.setSetting("dataset_info", "dataset", "full_set")
    dbHandler = DatabaseHandler(configHandler)
    return LabelStage(configHandler, dbHandler)

@pytest.fixture(scope="function")
def trainStage(tmpdir_factory, postgresql_my):
    pgtest = postgresql_my
    os.chdir(homePath)

    params = {
        "host": "127.0.0.1",
        "port": 5432,
        "database": "testDb",
        "user": "postgres",
        "password": "postgres"
    }
    connection = psycopg2.connect(**params)
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(open(imageLabelsBackupRelPath, "r").read())
    cursor.execute(open(featuresBackupRelPath, "r").read())

    direct = tmpdir_factory.mktemp("trainStage")
    directPath = str(direct)
    testConfigFullPath = directPath + os.path.sep + configFilename
    shutil.copyfile(configRelPath, testConfigFullPath)
    os.chdir(directPath)
    configHandler = CxrConfigHandler(testConfigFullPath)
    dbHandler = DatabaseHandler(configHandler)
    return TrainStage(configHandler, dbHandler)