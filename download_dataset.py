import requests
import tarfile
import os

URL = "https://openi.nlm.nih.gov/imgs/collections/NLMCXR_dcm.tgz"
FILENAME = URL.split("/")[-1]

def download_dataset():
    print("starting downloading")
    with requests.get(URL, stream=True) as r:
        r.raise_for_status()
        with open(FILENAME, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)

    if os.path.getsize('NLMCXR_dcm.tgz') != 80694582486:
        raise IOError('NLMCXR_dcm.tgz did not download properly!')

    print("download finished")

def unpack():
    print('unpacking')
    tf = tarfile.open("NLMCXR_dcm.tgz")
    tf.extractall(path='./NLMCXR_dcm')
    print('done unpacking')
    return os.path.dirname(os.path.abspath(__file__)) + '/NLMCXR_dcm'
