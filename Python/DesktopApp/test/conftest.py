import pytest
from pytest_postgresql import factories
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cxrConfigHandler import CxrConfigHandler
from metadata_to_db.databaseHandler import DatabaseHandler
from downloadStage import DownloadStage
from unpackStage import UnpackStage
from storeStage import StoreStage
import shutil


configFilename = "config.ini"
tgzFilename = "NLMCXR_subset_dataset.tgz"
dcmFolderName = tgzFilename.split(".")[0]
testDataRelPath = "./testData"
configRelPath = testDataRelPath + os.path.sep + configFilename
tgzRelPath = testDataRelPath + os.path.sep + tgzFilename
dcmFolderRelPath = testDataRelPath + os.path.sep + dcmFolderName
columnsInfoFilename = "columns_info.json"
columnsInfoRelPath = testDataRelPath + os.path.sep + columnsInfoFilename
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