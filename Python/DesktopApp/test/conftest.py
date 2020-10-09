import pytest
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
homePath = os.getcwd()

@pytest.fixture(scope="class")
def cxrConfigHandler():
    return CxrConfigHandler(configRelPath)

@pytest.fixture(scope="class")
def databaseHandler():
    configHandler = CxrConfigHandler(configRelPath)
    return DatabaseHandler(configHandler)

@pytest.fixture(scope="class")
def downloadStage(tmpdir_factory):
    os.chdir(homePath)
    direct = tmpdir_factory.mktemp("downloadStage")
    directPath = str(direct)
    testConfigFullPath = directPath + os.path.sep + configFilename
    shutil.copyfile(configRelPath, testConfigFullPath)
    os.chdir(str(direct))
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

@pytest.fixture(scope="class")
def storeStage():
    configHandler = CxrConfigHandler(configRelPath)
    dbHandler = DatabaseHandler(configHandler)
    return StoreStage(configHandler, dbHandler)

# @pytest.fixture(scope="session")
# def image_file(tmpdir_factory):
#     img = compute_expensive_image()
#     fn = tmpdir_factory.mktemp("data").join("img.png")
#     img.save(str(fn))
#     return fn