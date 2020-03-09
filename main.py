"""Contains the software coordinating the logic of the application."""
import logging
import os
import concurrent.futures
from download_dataset import DatasetController
from DicomToDatabase.dicom_to_db import dicom_to_db
from calculate_features import calculate_features
from LabelImages import LabelImageApplication
import DicomToDatabase.basic_db_ops as bdo
import DicomToDatabase.config as config
from classification import classification

class Controller():
    """Controller class that controls the logic of the application."""
    def __init__(self):
        logging.info('Initializing Controller')
        self.config_file_name = 'config.ini'
        self.columns_info = 'columns_info.json'
        self.label_app = None
        self.classifier = None
        # self.url = 'https://openi.nlm.nih.gov/imgs/collections/NLMCXR_dcm.tgz'
        self.url = 'https://github.com/Matt-Conrad/CXR_View_Classification/raw/master/NLMCXR_subset_dataset.tgz'
        self.dataset_controller = DatasetController(self.url)
        logging.info('Controller initialized')

    def download_dataset(self, feedback_dashboard):
        """Download the dataset (tgz format) from the public repository."""
        self.dataset_controller.get_dataset(feedback_dashboard)

    def unpack_dataset(self, feedback_dashboard):
        """Unpack the dataset from the tgz file."""
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            executor.submit(self.update_dashboard, feedback_dashboard)
            executor.submit(self.dataset_controller.unpack)
        config.update_config_file(filename=self.config_file_name, section='dicom_folder', key='folder_path', value=self.dataset_controller.folder_full_path)

    def update_dashboard(self, feedback_dashboard):
        while sum([len(files) for r, d, files in os.walk(self.dataset_controller.folder_full_path)]) < 10:
            num_files = sum([len(files) for r, d, files in os.walk(self.dataset_controller.folder_full_path)])
            feedback_dashboard.itemAt(1).widget().setValue(num_files)
        num_files = sum([len(files) for r, d, files in os.walk(self.dataset_controller.folder_full_path)])
        feedback_dashboard.itemAt(1).widget().setValue(num_files)
        
    def store_metadata(self):
        """Move all desired DCM tag-values from a directory full of DCMs into a PostgreSQL DB."""
        dicom_to_db(self.columns_info, self.config_file_name, 'elements')

    def calculate_features(self):
        """Calculate features for each image in the Postgres DB."""
        table_name = config.get_config_setting(self.config_file_name, section='table_info', key='features_table_name')
        bdo.add_table_to_db(table_name, self.columns_info, self.config_file_name, 'features_list')
        calculate_features(self.config_file_name)

    def label_images(self):
        """Use an app to manually label images."""
        table_name = config.get_config_setting(self.config_file_name, section='table_info', key='label_table_name')
        bdo.add_table_to_db(table_name, self.columns_info, self.config_file_name, 'labels')
        self.label_app = LabelImageApplication(self.config_file_name)

    def classification(self):
        """Performs the classification and gets the accuracy of the classifier."""
        self.classifier, accuracy = classification(self.config_file_name)
