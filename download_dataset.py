import requests
import tarfile

URL = "https://openi.nlm.nih.gov/imgs/collections/NLMCXR_dcm.tgz"
FILENAME = URL.split("/")[-1]

def download_dataset():
    with requests.get(URL, stream=True) as r:
        r.raise_for_status()
        with open(FILENAME, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)

def unpack():
    # subprocess.run(['mkdir', FILENAME.split('.')[0]])
    # subprocess.run(['tar', '-xzvf', 'NLMCXR_dcm.tgz', '-C', 'NLMCXR_dcm'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    tf = tarfile.open("NLMCXR_dcm.tgz")
    tf.extractall(path='./NLMCXR_dcm')

if __name__ == "__main__":
    print("starting downloading")
    # download_dataset()
    print("download finished")
    print('unpacking')
    unpack()
    print('done unpacking')