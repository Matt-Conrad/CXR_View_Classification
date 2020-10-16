import pytest
from expectedSizes import EXPECTED_NUM_FILES
from labelStage import LabelStage
from PyQt5.QtCore import QRunnable, QThreadPool
import time

class TestManualLabelStage:
    threadpool = QThreadPool()

    @pytest.fixture(autouse=True)
    def initLabelStage(self, manualLabelStage):
        self.labelStage = manualLabelStage
        self.labelBot = LabelBot(self.labelStage)

    def test_labelerIsManualLabeler(self):
        assert isinstance(self.labelStage.labeler, LabelStage.ManualLabeler)

    def test_dbExists(self):
        assert self.labelStage.labeler.dbHandler.dbExists(self.labelStage.labeler.configHandler.getDbInfo()["database"])

    def test_metaTableExists(self):
        assert self.labelStage.labeler.dbHandler.tableExists(self.labelStage.labeler.configHandler.getTableName("metadata"))

    def test_featureTableExists(self):
        assert self.labelStage.labeler.dbHandler.tableExists(self.labelStage.labeler.configHandler.getTableName("features"))

    def test_labelTableNotExists(self):
        assert not self.labelStage.labeler.dbHandler.tableExists(self.labelStage.labeler.configHandler.getTableName("label"))

    def test_manualLabeler(self):
        self.threadpool.start(self.labelStage.labeler)
        self.threadpool.start(self.labelBot)
        
        while not self.labelStage.labeler.dbHandler.tableExists(self.labelStage.labeler.configHandler.getTableName("label")):
            pass

        while self.labelStage.labeler.dbHandler.countRecords(self.labelStage.labeler.configHandler.getTableName("label")) < EXPECTED_NUM_FILES["subset"]:
            pass

        assert self.labelStage.labeler.dbHandler.tableExists(self.labelStage.labeler.configHandler.getTableName("label"))
        assert self.labelStage.labeler.dbHandler.countRecords(self.labelStage.labeler.configHandler.getTableName("label")) == EXPECTED_NUM_FILES["subset"]
        sqlQuery = 'SELECT * FROM ' + self.labelStage.labeler.configHandler.getTableName("label") + ' ORDER BY file_name ASC;'
        cursor = self.labelStage.labeler.dbHandler.executeQuery(self.labelStage.labeler.dbHandler.connection, sqlQuery)
        record = cursor.fetchone()
        assert record["file_name"] == "1_IM-0001-3001.dcm"
        assert record["file_path"] == "NLMCXR_subset_dataset/NLMCXR_subset_dataset/1/1_IM-0001-3001.dcm"
        assert record["image_view"] == "F"

class LabelBot(QRunnable):
    def __init__(self, labelStage):
        QRunnable.__init__(self)
        self.labelStage = labelStage
    
    def run(self):
        time.sleep(3)
        for i in range(EXPECTED_NUM_FILES["subset"]):
            if i % 2 == 0:
                self.labelStage.labeler.frontal()
            else:
                self.labelStage.labeler.lateral()
            time.sleep(1)