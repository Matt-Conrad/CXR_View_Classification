import logging
import tarfile
import os
import requests
import time

EXPECTED_SIZES = {
        'NLMCXR_subset_dataset.tgz': 88320855,
        'NLMCXR_dcm.tgz': 80694582486
    }

class DatasetController:
    """Controls logic of getting the dataset from online sources."""
    def __init__(self, url):
        self.expected_num_files = 10
        self.url = url
        self.filename = url.split("/")[-1]
        self.folder_name = self.filename.split('.')[0]
        self.folder_full_path = os.path.dirname(os.path.abspath(__file__)).replace('\\','/') + '/' + self.folder_name
        self.expected_size = EXPECTED_SIZES[self.filename]

    def get_dataset(self, feedback_dashboard):
        """Attempt to get the dataset TGZ as many times as it takes."""
        logging.info('Checking if %s already exists', self.filename)
        if os.path.isfile(self.filename):
            logging.info('%s already exists', self.filename)
            logging.info('Checking if %s was downloaded properly', self.filename)
            if os.path.getsize(self.filename) == self.expected_size:
                logging.info('%s was downloaded properly', self.filename)
            else:
                logging.warning('%s was NOT downloaded properly', self.filename)
                logging.info('Removing %s', self.filename)
                os.remove(self.filename)
                logging.info('Successfully removed %s', self.filename)
                self.download_dataset(feedback_dashboard)
        else:
            logging.info('%s does not exist', self.filename)
            self.download_dataset(feedback_dashboard)

    def download_dataset(self, feedback_dashboard):
        """Download the dataset, invoke the checks in get_dataset after."""
        # Start download
        logging.info('Downloading dataset from %s', self.url)
        
        with requests.get(self.url, stream=True) as r:
            r.raise_for_status()
            with open(self.filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192): 
                    if chunk: # filter out keep-alive new chunks
                        f.write(chunk)
                        feedback_dashboard.itemAt(1).widget().setValue(os.path.getsize(self.filename))
                        
        feedback_dashboard.itemAt(1).widget().setValue(os.path.getsize(self.filename))
        self.get_dataset(feedback_dashboard.itemAt(1).widget())
        return self.filename

    def unpack(self):
        logging.info('Unpacking dataset from %s', self.filename)
        tf = tarfile.open(self.filename)
        tf.extractall(path='./')
        logging.info('Done unpacking')
