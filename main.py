"""Contains the software coordinating the logic of the application."""
import logging
import os
import sys
from PyQt5.QtCore import QThreadPool
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from download_dataset import DatasetController
import DicomToDatabase.basic_db_ops as bdo
import DicomToDatabase.config as config
from main_gui import MainApplication
from download_button import download_functionality
from unpack_button import unpack_functionality
from store_button import store_functionality
from calculate_button import calculate_functionality
from label_button import label_functionality
from classification_button import classification_functionality

SOURCE_URL = {
        'subset': 'https://github.com/Matt-Conrad/CXR_View_Classification/raw/master/NLMCXR_subset_dataset.tgz',
        'full_set': 'https://openi.nlm.nih.gov/imgs/collections/NLMCXR_dcm.tgz'
    }

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
        self.config_file_name = 'config.ini'
        self.dataset = config.config(filename=self.config_file_name, section='dataset_info')['dataset']
        self.url = SOURCE_URL[self.dataset]

        # Object variables
        self.main_app = MainApplication()
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

        self.download_functionality = download_functionality(self)
        self.unpack_functionality = unpack_functionality(self)
        self.store_functionality = store_functionality(self)
        self.calculate_functionality = calculate_functionality(self)
        self.label_functionality = label_functionality(self)
        self.classification_functionality = classification_functionality(self)

        self.connect_buttons()

    def connect_buttons(self):
        """Connect the buttons in the GUI to the functions here."""
        self.main_app.download_btn.clicked.connect(self.download_functionality.download_dataset)
        self.main_app.unpack_btn.clicked.connect(self.unpack_functionality.unpack_dataset)
        self.main_app.store_btn.clicked.connect(self.store_functionality.store_metadata)
        self.main_app.features_btn.clicked.connect(self.calculate_functionality.calculate_features)
        self.main_app.label_btn.clicked.connect(self.label_functionality.label_images)
        self.main_app.classify_btn.clicked.connect(self.classification_functionality.classification)

    def log_gui_state(self, debug_level):
        """Log the state of the feedback in the GUI."""
        if debug_level == 'debug':
            logging.debug('Text: ' + self.main_app.msg_box.text())
            logging.debug('Progress bar value: ' + str(self.main_app.pro_bar.value()))

if __name__ == "__main__":
    # Get log level from config file
    log_level = config.config(filename='config.ini', section='logging')['level']
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