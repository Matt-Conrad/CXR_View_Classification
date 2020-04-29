"""Provides the functionality of the unpack button."""
import os
import time
import logging
from workers import Worker, Updater

class unpack_functionality():
    def __init__(self, controller):
        self.controller = controller

    def unpack_dataset(self):
        """Delegate the unpacking and GUI updating to 2 new threads."""
        logging.info('***BEGIN UNPACKING PHASE***')
        # Set the progress region
        self.controller.main_app.msg_box.setText('Unpacking images')
        self.controller.main_app.pro_bar.setMinimum(0)
        self.controller.main_app.pro_bar.setMaximum(self.controller.dataset_controller.expected_num_files)

        # Create 2 workers: 1 to unpack and 1 to update the progress bar
        worker = Worker(self.unpack)
        updater = Updater(self.update_unpack)
        # Connect the updater signal to the progress bar
        updater.signals.progress.connect(self.controller.main_app.update_pro_bar)
        updater.signals.finished.connect(self.controller.main_app.update_text)
        # Start the threads
        self.controller.threadpool.start(worker)
        self.controller.threadpool.start(updater)

    def unpack(self):
        """Unpack the image set."""
        self.controller.dataset_controller.unpack()

    def update_unpack(self, progress_callback, finished_callback):
        """Updates the GUI's progress bar.

        Parameters
        ----------
        progress_callback : pyqtSignal(int)
            Used to emit a signal to the GUI to update the progress bar. Passed automatically by Updater class.
        finished_callback : pyqtSignal(int)
            Used to emit a signal to the GUI to update the text. Passed automatically by Updater class.
        """
        # Wait for the folder to be available before updating progress bar
        while not os.path.isdir(self.controller.dataset_controller.folder_full_path):
            logging.debug('waiting')
            time.sleep(1)
            pass

        # Update the progress bar with the current file count in the folder path
        progress_callback.emit(0)
        self.controller.log_gui_state('debug')
        while self.count_DCMs(self.controller.dataset_controller.folder_full_path) < self.controller.dataset_controller.expected_num_files:
            progress_callback.emit(self.count_DCMs(self.controller.dataset_controller.folder_full_path))
            self.controller.log_gui_state('debug')
            time.sleep(1)
        progress_callback.emit(self.count_DCMs(self.controller.dataset_controller.folder_full_path))
        logging.debug('Final count: ' + str(self.count_DCMs(self.controller.dataset_controller.folder_full_path)))

        # Update the text and move to the next stage
        finished_callback.emit('Images unpacked')
        self.controller.log_gui_state('debug')
        logging.info('***END UNPACKING PHASE***')
        self.controller.main_app.stage3_ui()

    def count_DCMs(self, full_folder_path):
        return sum([len(files) for r, d, files in os.walk(full_folder_path) if any(item.endswith('.dcm') for item in files)])
