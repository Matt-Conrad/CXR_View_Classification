"""Provides the functionality of the download button."""
import os
import time
import logging
import DicomToDatabase.config as config
from workers import Worker, Updater

class download_functionality():
    def __init__(self, controller):
        self.controller = controller

    def download_dataset(self):
        """Delegate the downloading and GUI updating to 2 new threads."""
        logging.info('***BEGIN DOWNLOADING PHASE***')
        # Set the progress region
        self.controller.main_app.msg_box.setText('Downloading images')
        self.controller.main_app.pro_bar.setMinimum(0)
        self.controller.main_app.pro_bar.setMaximum(self.get_tgz_max())
        
        # Create 2 workers: 1 to download and 1 to update the progress bar
        worker = Worker(self.download)
        updater = Updater(self.update)
        # Connect the updater signal to the progress bar
        updater.signals.progress.connect(self.controller.main_app.update_pro_bar)
        updater.signals.finished.connect(self.controller.main_app.update_text)
        # Start the threads
        self.controller.threadpool.start(worker)
        self.controller.threadpool.start(updater)

    def download(self):
        """Download the image set."""
        self.controller.dataset_controller.get_dataset()
        config.update_config_file(self.controller.config_file_name, 'dicom_folder', 'folder_path', self.controller.dataset_controller.folder_full_path)

    def update(self, progress_callback, finished_callback):
        """Updates the GUI's progress bar.

        Parameters
        ----------
        progress_callback : pyqtSignal(int)
            Used to emit a signal to the GUI to update the progress bar. Passed automatically by Updater class.
        finished_callback : pyqtSignal(int)
            Used to emit a signal to the GUI to update the text. Passed automatically by Updater class.
        """
        # Wait for the file to start downloading before updating progress bar
        while not os.path.exists(self.controller.dataset_controller.filename_fullpath):
            pass

        # Update the progress bar with the current file size
        progress_callback.emit(0)
        self.controller.log_gui_state('debug')
        while self.get_tgz_size() < self.get_tgz_max():
            progress_callback.emit(self.get_tgz_size())
            self.controller.log_gui_state('debug')
            time.sleep(1)
        progress_callback.emit(self.get_tgz_size())

        # Update the text and move to the next stage
        finished_callback.emit('Image download complete')
        self.controller.log_gui_state('debug')
        logging.info('***END DOWNLOADING PHASE***')
        self.controller.main_app.stage2_ui()

    def get_tgz_size(self):
        """Calculates the size of the TGZ file for the purpose of setting the progress bar value."""
        if self.controller.dataset == 'full_set':
            # Dividing by 100 because the expected size of this TGZ is larger than QProgressBar accepts
            return int(os.path.getsize(self.controller.dataset_controller.filename_fullpath) / 100)
        elif self.controller.dataset == 'subset':
            return os.path.getsize(self.controller.dataset_controller.filename_fullpath)
        else:
            raise ValueError('Value must be one of the keys in SOURCE_URL')

    def get_tgz_max(self):
        """Calculates the size of the TGZ file max for the purpose of setting the progress bar max."""
        if self.controller.dataset == 'full_set':
            # Dividing by 100 because the expected size of this TGZ is larger than QProgressBar accepts
            return int(self.controller.dataset_controller.expected_size / 100)
        elif self.controller.dataset == 'subset':
            return self.controller.dataset_controller.expected_size
        else:
            raise ValueError('Value must be one of the keys in SOURCE_URL')