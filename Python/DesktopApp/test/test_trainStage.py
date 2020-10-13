import pytest
import os
from expectedSizes import EXPECTED_SIZES, EXPECTED_NUM_FILES
from PyQt5.QtCore import QObject, pyqtSlot

class TestTrainStage:
    @pytest.fixture(autouse=True)
    def initTrainStage(self, trainStage):
        self.trainStage = trainStage
        self.listener = Listener()
        os.chdir(self.trainStage.trainer.configHandler.getParentFolder())

    def test_dbExists(self):
        assert self.trainStage.trainer.dbHandler.dbExists(self.trainStage.trainer.configHandler.getDbInfo()["database"])

    def test_featureTableExists(self):
        assert self.trainStage.trainer.dbHandler.tableExists(self.trainStage.trainer.configHandler.getTableName("features"))

    def test_labelTableExists(self):
        assert self.trainStage.trainer.dbHandler.tableExists(self.trainStage.trainer.configHandler.getTableName("label"))

    def test_trainStage(self):
        # Separate these asserts into multiple tests
        self.trainStage.trainer.signals.attemptUpdateText.connect(self.listener.validateTrainResult)
        self.trainStage.trainer.run()
        assert self.listener.result >= 0.0
        assert self.listener.result <= 1.0

    
class Listener(QObject):
    def __init__(self):
        QObject.__init__(self)
        self.result = None

    @pyqtSlot(str)
    def validateTrainResult(self, text):
        if text != "Training classifier":
            self.result = float(text.replace("K-Fold Cross Validation Accuracy: ", ""))
