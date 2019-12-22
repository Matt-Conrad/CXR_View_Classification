from download_dataset import download_dataset, unpack
from dicom_to_db import dicom_to_db
from calculate_features import calculate_features
from LabelImages import run_app

class controller:
    def __init__(self):
        pass

    def download_dataset(self):
        """Download the dataset (tgz format) from the public repository."""
        print("starting downloading")
        download_dataset()
        print("download finished")

    def unpack_dataset(self):
        """Unpack the dataset from the tgz file."""
        print('unpacking')
        unpack()
        print('done unpacking')

    def store_metadata(self):
        """Move all desired DCM tag-values from a directory full of DCMs into a PostgreSQL DB."""
        dicom_to_db('elements.json', 'config.ini')

    def calculate_features(self):
        """Calculate features for each image in the Postgres DB."""
        calculate_features('config.ini')

    def label_images(self):
        """Use an app to manually label images."""
        run_app()
