from download_dataset import download_dataset, unpack
from dicom_to_db import dicom_to_db
from calculate_features import calculate_features
from LabelImages import run_app
import basic_db_ops as bdo
import config
from classification import classification

class controller:
    def __init__(self):
        self.config_file_name = 'config.ini'
        self.elements_json = 'elements.json'
        self.features_list = 'features_list.json'
        self.label = 'label.json'
        self.classifier = None

    def download_dataset(self):
        """Download the dataset (tgz format) from the public repository."""
        download_dataset()

    def unpack_dataset(self):
        """Unpack the dataset from the tgz file."""
        folder = unpack()
        config.update_config_file(filename=self.config_file_name, section='dicom_folder', key='folder_path', value=folder)

    def store_metadata(self):
        """Move all desired DCM tag-values from a directory full of DCMs into a PostgreSQL DB."""
        db_name = 'test'
        bdo.create_new_db(db_name)
        config.update_config_file(filename=self.config_file_name, section='postgresql', key='database', value=db_name)
        table_name = config.get_config_setting(self.config_file_name, section='table_info', key='table_name')
        bdo.add_table_to_db(table_name, self.elements_json, self.config_file_name)
        dicom_to_db(self.elements_json, self.config_file_name)

    def calculate_features(self):
        """Calculate features for each image in the Postgres DB."""
        table_name = config.get_config_setting(self.config_file_name, section='feature_table_info', key='table_name')
        bdo.add_table_to_db(table_name, self.features_list, self.config_file_name)
        calculate_features(self.config_file_name)

    def label_images(self):
        """Use an app to manually label images."""
        table_name = config.get_config_setting(self.config_file_name, section='label_table_info', key='table_name')
        bdo.add_table_to_db(table_name, self.label, self.config_file_name)
        run_app(self.config_file_name)

    def classification(self):
        """Performs the classification and gets the accuracy of the classifier."""
        self.classifier, accuracy = classification(self.config_file_name)
        print(accuracy)

if __name__ == "__main__":
    controller = controller()
    controller.label_images()
