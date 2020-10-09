import pytest
import os
from expectedSizes import EXPECTED_SIZES, EXPECTED_NUM_FILES
    
class TestStoreStage:
    @pytest.fixture(autouse=True)
    def initStoreStage(self, storeStage):
        self.storeStage = storeStage

    def test_tgzExistsBeforeStore(self):
        assert os.path.isfile(self.storeStage.storer.configHandler.getTgzFilename())
    
    def test_tgzUnpackedBeforeStore(self):
        folderName = self.storeStage.storer.configHandler.getDatasetName()
        assert sum([len(files) for r, d, files in os.walk(folderName) if any(item.endswith('.dcm') for item in files)]) == EXPECTED_NUM_FILES["subset"]

    def test_metaTableNotExists(self):
        assert not self.storeStage.storer.dbHandler.tableExists(self.storeStage.storer.configHandler.getTableName("metadata"))

    def test_store(self):
        self.storeStage.storer.run()
        assert self.storeStage.storer.dbHandler.tableExists(self.storeStage.storer.configHandler.getTableName("metadata"))

    