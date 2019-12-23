from download_dataset import download_dataset, unpack
from dicom_to_db import dicom_to_db
from calculate_features import calculate_features
from LabelImages import run_app
import basic_db_ops as bdo
import config

class controller:
    def __init__(self):
        self.config_file_name = 'config.ini'

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
        bdo.add_table_to_db('image_metadata', 'elements.json', self.config_file_name)
        dicom_to_db('elements.json', 'config.ini')

    def calculate_features(self):
        """Calculate features for each image in the Postgres DB."""
        calculate_features('config.ini')

    def label_images(self):
        """Use an app to manually label images."""
        run_app()

if __name__ == "__main__":
    controller = controller()
    controller.store_metadata()
