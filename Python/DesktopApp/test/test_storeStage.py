import pytest
import os
from expectedSizes import EXPECTED_SIZES, EXPECTED_NUM_FILES
    
def countDcms(folderName):
    return sum([len(files) for r, d, files in os.walk(folderName) if any(item.endswith('.dcm') for item in files)])

class TestStoreStage:
    @pytest.fixture(autouse=True)
    def initStoreStage(self, storeStage):
        self.storeStage = storeStage
    
    def test_tgzUnpackedBeforeStore(self):
        folderName = self.storeStage.storer.configHandler.getUnpackFolderPath()
        assert countDcms(folderName) == EXPECTED_NUM_FILES["subset"]

    def test_dbExists(self):
        assert self.storeStage.storer.dbHandler.dbExists(self.storeStage.storer.configHandler.getDbInfo()["database"])

    def test_metaTableNotExists(self):
        assert not self.storeStage.storer.dbHandler.tableExists(self.storeStage.storer.configHandler.getTableName("metadata"))

    def test_store(self):
        # Separate these asserts into multiple tests
        self.storeStage.storer.run()
        assert self.storeStage.storer.dbHandler.tableExists(self.storeStage.storer.configHandler.getTableName("metadata"))
        assert self.storeStage.storer.dbHandler.countRecords(self.storeStage.storer.configHandler.getTableName("metadata")) == EXPECTED_NUM_FILES["subset"]
        
        sqlQuery = 'SELECT * FROM ' + self.storeStage.storer.configHandler.getTableName("metadata") + ' ORDER BY file_name ASC;'
        cursor = self.storeStage.storer.dbHandler.executeQuery(self.storeStage.storer.dbHandler.connection, sqlQuery)
        record = cursor.fetchone()
        assert record["file_name"] == "1_IM-0001-3001.dcm"
        assert record["file_path"] == os.path.join(self.storeStage.storer.configHandler.getParentFolder(), "NLMCXR_subset_dataset", "NLMCXR_subset_dataset", "1", "1_IM-0001-3001.dcm")
        assert record["patient_orientation"] == "L\\F"
        assert record["view_position"] == "PA"
        assert record["modality"] == "CR"
        assert record["bits_stored"] == 15
        assert record["photometric_interpretation"] == "MONOCHROME1"
        assert record["window_center"] == None
        assert record["window_width"] == None

        record = cursor.fetchone()
        record = cursor.fetchone()
        assert record["window_center"] == 3134
        assert record["window_width"] == 1646

        

    