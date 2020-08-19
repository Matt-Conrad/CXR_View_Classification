from PyQt5.QtCore import QObject, pyqtSignal
from expected_sizes import EXPECTED_NUM_FILES, EXPECTED_SIZES

class Stage(QObject):
    """Contains GUI code for the application."""
    # Signals
    finished = pyqtSignal()
    attemptUpdateProBarValue = pyqtSignal(int)
    attemptUpdateProBarBounds = pyqtSignal(int, int)
    attemptUpdateText = pyqtSignal(str)

    def __init__(self, configHandler, dbHandler=None):
        QObject.__init__(self)
        self.configHandler = configHandler
        self.dbHandler = dbHandler

        self.expected_size = EXPECTED_SIZES[self.configHandler.getDatasetType()]
        self.expected_num_files = EXPECTED_NUM_FILES[self.configHandler.getDatasetType()]


