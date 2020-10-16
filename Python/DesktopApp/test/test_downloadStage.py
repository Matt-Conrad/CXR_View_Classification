import pytest
import os
from expectedSizes import EXPECTED_SIZES
    
class TestDownloadStage:
    @pytest.fixture(autouse=True)
    def initDownloadStage(self, downloadStage):
        self.downloadStage = downloadStage

    def test_noTgzBeforeDownload(self):
        assert not os.path.isfile(self.downloadStage.downloader.configHandler.getTgzFilePath())

    def test_getTgzSizeBeforeDownload(self):
        assert self.downloadStage.downloader.getTgzSize() is None

    def test_download(self):
        self.downloadStage.downloader.run()
        assert os.path.isfile(self.downloadStage.downloader.configHandler.getTgzFilePath())

    def test_getTgzSizeAfterDownload(self):
        assert self.downloadStage.downloader.getTgzSize() == EXPECTED_SIZES["subset"]

    def test_getTgzMax(self):
        assert self.downloadStage.downloader.getTgzMax() == EXPECTED_SIZES["subset"]
