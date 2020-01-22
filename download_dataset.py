import logging
import requests
import tarfile
import os
import logging

def download_dataset(url):
    # Start download
    logging.info('Downloading dataset from %s', url)

    filename = url.split("/")[-1]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)

    # if os.path.getsize('NLMCXR_dcm.tgz') != 80694582486:
    #     raise IOError('NLMCXR_dcm.tgz did not download properly!')

    logging.info('Download successful')

    return filename

def unpack(filename):
    logging.info('Unpacking dataset from %s', filename)
    tf = tarfile.open(filename)
    folder_name = filename.split('.')[0]
    tf.extractall(path='./' + folder_name)
    logging.info('Done unpacking')

    return os.path.dirname(os.path.abspath(__file__)) + '/' + folder_name
