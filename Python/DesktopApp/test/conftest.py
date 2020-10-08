import pytest
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cxrConfigHandler import CxrConfigHandler
from downloadStage import DownloadStage
from unpackStage import UnpackStage

configRelPath = "../../../miscellaneous/config.ini"

@pytest.fixture(scope="class")
def cxrConfigHandler():
    return CxrConfigHandler(configRelPath)

@pytest.fixture(scope="class")
def downloadStage():
    configHandler = CxrConfigHandler(configRelPath)
    return DownloadStage(configHandler)

@pytest.fixture(scope="class")
def unpackStage():
    configHandler = CxrConfigHandler(configRelPath)
    return UnpackStage(configHandler)
    