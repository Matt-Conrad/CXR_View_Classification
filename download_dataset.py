import requests
import tarfile
import os

# URL = "https://openi.nlm.nih.gov/imgs/collections/NLMCXR_dcm.tgz"
# FILENAME = URL.split("/")[-1]

def download_dataset(url):
    print("starting downloading")
    filename = url.split("/")[-1]
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)

    # if os.path.getsize('NLMCXR_dcm.tgz') != 80694582486:
    #     raise IOError('NLMCXR_dcm.tgz did not download properly!')

    print("download finished")
    return filename

def unpack(filename):
    print('unpacking')
    tf = tarfile.open(filename)
    folder_name = filename.split('.')[0]
    tf.extractall(path='./' + folder_name)
    print('done unpacking')
    return os.path.dirname(os.path.abspath(__file__)) + '/' + folder_name
