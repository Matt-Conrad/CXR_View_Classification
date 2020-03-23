"""Handles the acquiring of the image set."""
import logging
import tarfile
import os
import requests

# Hard-coded values for file size and file count for each TGZ
EXPECTED_SIZES = {
        'NLMCXR_subset_dataset.tgz': 88320855,
        'NLMCXR_dcm.tgz': 80694582486
    }

EXPECTED_NUM_FILES = {
        'NLMCXR_subset_dataset.tgz': 10,
        'NLMCXR_dcm.tgz': 1939 #3852 cut in half for testing purposes
    }

class DatasetController:
    """Controls logic of getting the dataset from online sources."""
    def __init__(self, url):
        # String variables file locations
        self.url = url
        self.parent_folder = os.path.dirname(os.path.abspath(__file__)).replace('\\','/')
        self.filename = url.split("/")[-1]
        self.filename_fullpath = self.parent_folder + '/' + self.filename
        self.folder_name = self.filename.split('.')[0]
        self.folder_full_path = self.parent_folder + '/' + self.folder_name
        self.columns_info_name = 'columns_info.json'
        self.columns_info_full_path = self.parent_folder + '/' + self.columns_info_name

        # Automatically oad the expected size into object
        self.expected_size = EXPECTED_SIZES[self.filename]
        self.expected_num_files = EXPECTED_NUM_FILES[self.filename]

    def get_dataset(self):
        """Attempt to get the dataset TGZ as many times as it takes. This one gets called by main.py"""
        logging.info('Checking if %s already exists', self.filename_fullpath)
        if os.path.isfile(self.filename_fullpath):
            logging.info('%s already exists', self.filename_fullpath)
            logging.info('Checking if %s was downloaded properly', self.filename_fullpath)
            
            if os.path.getsize(self.filename_fullpath) == self.expected_size:
                logging.info('%s was downloaded properly', self.filename_fullpath)
            else:
                logging.warning('%s was NOT downloaded properly', self.filename_fullpath)
                logging.info('Removing %s', self.filename_fullpath)
                os.remove(self.filename_fullpath)
                logging.info('Successfully removed %s', self.filename_fullpath)
                self.download_dataset()
        else:
            logging.info('%s does not exist', self.filename_fullpath)
            self.download_dataset()

    def download_dataset(self):
        """Download the dataset, invoke the checks in get_dataset after.
        
        This runs after get_dataset figures out the current state of the downloading.
        """
        # Start download
        logging.info('Downloading dataset from %s', self.url)
        with requests.get(self.url, stream=True) as r:
            r.raise_for_status() # Raise error if something goes wrong with connection
            with open(self.filename_fullpath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)
                    
        self.get_dataset()

    def unpack(self):
        """Unpack the dataset from the TGZ and put it in a folder."""
        logging.info('Unpacking dataset from %s', self.filename_fullpath)
        tf = tarfile.open(self.filename_fullpath)
        tf.extractall(path=self.folder_full_path)
        logging.info('Done unpacking')
