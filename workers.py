"""Contains worker thread classes that allow the GUI to run multi-threaded utilities."""
import sys
import traceback
from PyQt5.QtCore import QObject, QRunnable, pyqtSlot, pyqtSignal

class Worker(QRunnable):
    """Class that runs worker threads.

    From https://www.learnpyqt.com/courses/concurrent-execution/multithreading-pyqt-applications-qthreadpool/
    """
    def __init__(self, fn, *args, **kwargs):
        # super(Worker, self).__init__()
        QRunnable.__init__(self)
        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    @pyqtSlot()
    def run(self):
        """Initialise the runner function with passed args, kwargs."""
        try:
            self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            print(exctype, value)

class Updater(Worker):
    """Class that runs worker threads and emits updates for progress bar and text updates."""
    def __init__(self, fn, *args, **kwargs):
        Worker.__init__(self, fn, *args, **kwargs)

        # Add the callback to our kwargs
        self.signals = WorkerSignals()
        self.kwargs['progress_callback'] = self.signals.progress # Passes the progress signal to the function
        self.kwargs['finished_callback'] = self.signals.finished # Passes the finished signal to the function  

class WorkerSignals(QObject):
    """Container class for signals used by the Updater class."""
    progress = pyqtSignal(int)
    finished = pyqtSignal(str)