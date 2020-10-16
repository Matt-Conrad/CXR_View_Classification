import pytest
from expectedSizes import EXPECTED_NUM_FILES
from labelStage import LabelStage

class TestLabelImporter:
    @pytest.fixture(autouse=True)
    def initLabelStage(self, importLabelStage):
        self.labelStage = importLabelStage

    def test_labelerIsLabelImporter(self):
        assert isinstance(self.labelStage.labeler, LabelStage.LabelImporter)

    def test_dbExists(self):
        assert self.labelStage.labeler.dbHandler.dbExists(self.labelStage.labeler.configHandler.getDbInfo()["database"])

    def test_metaTableNotExists(self):
        assert not self.labelStage.labeler.dbHandler.tableExists(self.labelStage.labeler.configHandler.getTableName("metadata"))

    def test_featureTableNotExists(self):
        assert not self.labelStage.labeler.dbHandler.tableExists(self.labelStage.labeler.configHandler.getTableName("features"))

    def test_labelTableNotExists(self):
        assert not self.labelStage.labeler.dbHandler.tableExists(self.labelStage.labeler.configHandler.getTableName("label"))

    def test_manualLabeler(self):
        self.labelStage.labeler.run()
        assert self.labelStage.labeler.dbHandler.tableExists(self.labelStage.labeler.configHandler.getTableName("label"))
        assert self.labelStage.labeler.dbHandler.countRecords(self.labelStage.labeler.configHandler.getTableName("label")) == EXPECTED_NUM_FILES["full_set"]
        
        sqlQuery = 'SELECT * FROM ' + self.labelStage.labeler.configHandler.getTableName("label") + ' ORDER BY file_name ASC;'
        cursor = self.labelStage.labeler.dbHandler.executeQuery(self.labelStage.labeler.dbHandler.connection, sqlQuery)
        record = cursor.fetchone()
        assert record["file_name"] == "1000_IM-0003-1001.dcm"
        assert record["file_path"] == "/home/matthew/Documents/Datasets/NLMCXR_dcm/1000/1000_IM-0003-1001.dcm"
        assert record["image_view"] == "F"