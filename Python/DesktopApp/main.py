"""Contains the software coordinating the logic of the application."""
import logging
import os
import sys
from PyQt5.QtCore import QThreadPool
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from download_dataset import DatasetController
import metadata_to_db.basic_db_ops as bdo
import metadata_to_db.config as config
from main_window import MainWindow

SOURCE_URL = {
        'subset': 'https://github.com/Matt-Conrad/CXR_View_Classification/raw/develop/datasets/NLMCXR_subset_dataset.tgz',
        'full_set': 'https://openi.nlm.nih.gov/imgs/collections/NLMCXR_dcm.tgz'
    }

CONFIG_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')

def run_app():
    """Run the application that guides the user through the process."""
    app = QApplication(sys.argv)
    cont = Controller()
    app.exec_()

class Controller():
    """Controller class that controls the logic of the application."""
    def __init__(self):
        logging.info('***INITIALIZING CONTROLLER***')

        # String variables
        self.config_file_name = CONFIG_NAME
        self.dataset = config.config(filename=self.config_file_name, section='dataset_info')['dataset']
        self.url = SOURCE_URL[self.dataset]

        # Object variables
        self.main_app = MainWindow(self)
        self.label_app = None
        self.classifier = None
        self.dataset_controller = DatasetController(self.url)

        # From config file
        self.db_name = config.config(filename=self.config_file_name, section='postgresql')['database']
        self.meta_table_name = config.config(filename=self.config_file_name, section='table_info')['metadata_table_name']
        self.feat_table_name = config.config(filename=self.config_file_name, section='table_info')['features_table_name']
        self.label_table_name = config.config(filename=self.config_file_name, section='table_info')['label_table_name']

        # Set up the GUI
        self.init_gui_state()
        self.threadpool = QThreadPool()
        logging.info('***CONTROLLER INITIALIZED***')

    ### GUI HELPER FUNCTIONS
    def init_gui_state(self):
        """Initialize the GUI in the right stage."""
        # Set icon
        self.main_app.setWindowIcon(QIcon(self.dataset_controller.parent_folder + '/' + 'icon.jpg'))

        if not os.path.exists(self.dataset_controller.filename) and not os.path.isdir(self.dataset_controller.folder_name) and not bdo.table_exists(self.config_file_name, self.db_name, self.meta_table_name): # If the TGZ hasn't been downloaded
            self.main_app.stage1_ui()
        elif os.path.exists(self.dataset_controller.filename) and not os.path.isdir(self.dataset_controller.folder_name) and not bdo.table_exists(self.config_file_name, self.db_name, self.meta_table_name):
            self.main_app.stage2_ui()
        elif os.path.exists(self.dataset_controller.filename) and os.path.isdir(self.dataset_controller.folder_name) and not bdo.table_exists(self.config_file_name, self.db_name, self.meta_table_name):
            self.main_app.stage3_ui()
        elif os.path.exists(self.dataset_controller.filename) and os.path.isdir(self.dataset_controller.folder_name) and bdo.table_exists(self.config_file_name, self.db_name, self.meta_table_name) and not bdo.table_exists(self.config_file_name, self.db_name, self.feat_table_name):
            self.main_app.stage4_ui()
        elif os.path.exists(self.dataset_controller.filename) and os.path.isdir(self.dataset_controller.folder_name) and bdo.table_exists(self.config_file_name, self.db_name, self.feat_table_name) and bdo.table_exists(self.config_file_name, self.db_name, self.feat_table_name) and not bdo.table_exists(self.config_file_name, self.db_name, self.label_table_name):
            self.main_app.stage5_ui()
        elif os.path.exists(self.dataset_controller.filename) and os.path.isdir(self.dataset_controller.folder_name) and bdo.table_exists(self.config_file_name, self.db_name, self.feat_table_name) and bdo.table_exists(self.config_file_name, self.db_name, self.feat_table_name) and bdo.table_exists(self.config_file_name, self.db_name, self.feat_table_name):
            self.main_app.stage6_ui()

    def log_gui_state(self, debug_level):
        """Log the state of the feedback in the GUI."""
        if debug_level == 'debug':
            logging.debug('Text: ' + self.main_app.msg_box.text())
            logging.debug('Progress bar value: ' + str(self.main_app.pro_bar.value()))

if __name__ == "__main__":
    # Get log level from config file
    log_level = config.config(filename=CONFIG_NAME, section='logging')['level']
    if log_level == 'debug':
        log_level_obj = logging.DEBUG
    elif log_level == 'info':
        log_level_obj = logging.INFO
    
    # Remove any log handlers to make way for our logger
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)
    
    # Set the logging
    logging.basicConfig(filename='CXR_Classification.log', level=log_level_obj,
                        format='%(asctime)s %(levelname)-8s: %(message)s', datefmt='%Y-%m-%d|%H:%M:%S')

    # Run the application
    run_app()