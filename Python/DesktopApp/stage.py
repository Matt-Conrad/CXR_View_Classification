from PyQt5.QtCore import QObject, pyqtSignal, QRunnable, QThreadPool
from expectedSizes import EXPECTED_NUM_FILES, EXPECTED_SIZES

class Stage(QObject):
    """Code for stage of the CXR training process."""
    threadpool = QThreadPool()

    def __init__(self):
        QObject.__init__(self)

class Runnable(QRunnable):
    """Code for stage of the CXR training process."""
    def __init__(self, configHandler, dbHandler=None):
        QRunnable.__init__(self)
        self.signals = Signals()
        self.configHandler = configHandler
        self.dbHandler = dbHandler

        self.expectedSize = EXPECTED_SIZES[self.configHandler.getDatasetType()]
        self.expectedNumFiles = EXPECTED_NUM_FILES[self.configHandler.getDatasetType()]

class Signals(QObject):
    finished = pyqtSignal()
    attemptUpdateProBarValue = pyqtSignal(int)
    attemptUpdateProBarBounds = pyqtSignal(int, int)
    attemptUpdateText = pyqtSignal(str)
    attemptUpdateImage = pyqtSignal(object)


