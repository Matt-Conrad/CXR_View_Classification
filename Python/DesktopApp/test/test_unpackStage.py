import pytest
import os
from expectedSizes import EXPECTED_SIZES, EXPECTED_NUM_FILES
    
class TestUnpackStage:
    @pytest.fixture(autouse=True)
    def initUnpackStage(self, unpackStage):
        self.unpackStage = unpackStage

    def test_tgzExistsBeforeUnpack(self):
        assert os.path.isfile(self.unpackStage.unpacker.configHandler.getTgzFilePath())
    
    def test_tgzFullyDownloadedBeforeUnpack(self):
        assert os.path.getsize(self.unpackStage.unpacker.configHandler.getTgzFilePath()) == EXPECTED_SIZES["subset"]
    
    def test_folderNotExistsBeforeUnpack(self):
        assert not os.path.exists(self.unpackStage.unpacker.configHandler.getUnpackFolderPath())

    def test_unpack(self):
        self.unpackStage.unpacker.run()
        assert os.path.exists(self.unpackStage.unpacker.configHandler.getUnpackFolderPath())

    def test_tgzFullyDownloadedAfterUnpack(self):
        assert os.path.getsize(self.unpackStage.unpacker.configHandler.getTgzFilePath()) == EXPECTED_SIZES["subset"]

    def test_folderAfterUnpack(self):
        assert self.unpackStage.unpackUpdater.countDcms() == EXPECTED_NUM_FILES["subset"]

    