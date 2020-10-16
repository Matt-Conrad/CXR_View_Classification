import pytest
import os

class TestCxrConfigHandler:
    @pytest.fixture(autouse=True)
    def initConfigHandler(self, cxrConfigHandler):
        self.cxrConfigHandler = cxrConfigHandler

    # Test get functions
    def test_getUrl(self):
        assert self.cxrConfigHandler.getUrl() == "https://github.com/Matt-Conrad/CXR_View_Classification/raw/develop/datasets/NLMCXR_subset_dataset.tgz"

    def test_getParentFolder(self):
        assert self.cxrConfigHandler.getParentFolder() == os.path.dirname(self.cxrConfigHandler.getConfigFilePath())

    def test_getCsvPath(self):
        assert self.cxrConfigHandler.getCsvPath() == os.path.join(self.cxrConfigHandler.getParentFolder(),"image_labels.csv")

    def test_getCsvName(self):
        assert self.cxrConfigHandler.getCsvName() == "image_labels.csv"

    def test_getColumnsInfoName(self):
        assert self.cxrConfigHandler.getColumnsInfoName() == "columns_info.json"

    def test_getDbInfo(self):
        expectedDbInfo = {
            "host": "127.0.0.1",
            "port": "5432",
            "database": "testDb",
            "user": "postgres",
            "password": "postgres",
        }
        assert self.cxrConfigHandler.getDbInfo() == expectedDbInfo

    def test_getTableName(self):
        assert self.cxrConfigHandler.getTableName("metadata") == "image_metadata"

    def test_getTgzFilename(self):
        assert self.cxrConfigHandler.getTgzFilename() == "NLMCXR_subset_dataset.tgz"

    def test_getTgzFilePath(self):
        assert self.cxrConfigHandler.getTgzFilePath() == os.path.join(self.cxrConfigHandler.getParentFolder(), "NLMCXR_subset_dataset.tgz")

    def test_getDatasetName(self):
        assert self.cxrConfigHandler.getDatasetName() == "NLMCXR_subset_dataset"

    def test_getUnpackFolderPath(self):
        assert self.cxrConfigHandler.getUnpackFolderPath() == os.path.join(self.cxrConfigHandler.getParentFolder(), "NLMCXR_subset_dataset")

    def test_getDatasetType(self):
        assert self.cxrConfigHandler.getDatasetType() == "subset"

    def test_getLogLevel(self):
        assert self.cxrConfigHandler.getLogLevel() == "info"

    # Test set functions
    def test_setUrl(self):
        text = "setUrl"
        self.cxrConfigHandler.setUrl(text)
        assert self.cxrConfigHandler.getUrl() == text

    def test_setParentFolder(self):
        self.cxrConfigHandler.setParentFolder()
        assert self.cxrConfigHandler.getParentFolder() == os.path.dirname(self.cxrConfigHandler.getConfigFilePath())

    def test_setCsvName(self):
        self.cxrConfigHandler.setCsvName()
        assert self.cxrConfigHandler.getCsvName() == "image_labels.csv"

    def test_setColumnsInfoName(self):
        self.cxrConfigHandler.setColumnsInfoName()
        assert self.cxrConfigHandler.getColumnsInfoName() == "columns_info.json"
