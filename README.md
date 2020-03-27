# Implementation of Chest X-ray Image View Classification
This project is an implementation of the paper "Chest X-ray Image View Classification" by Xue et al found [here](https://www.researchgate.net/publication/283778178_Chest_X-ray_Image_View_Classification). Currently, the implementation is in the form of an application that allows a user to interact with a GUI to go through the all of the steps including: downloading, storing metadata, extracting features, data labaling, classifier training, and classification.  

## Motivation
The inspiration for this project arises from my experience in the medical imaging industry. A classifier such as this would be useful in industry. One use case being a lot of medical imaging software relies on DICOM tags such as laterality (0020,0060), view position (0018,5101), and patient orientation (0020,0020) to perform some action. However, this tag is not always there such as in the image set from [NLM History of Medicine](https://openi.nlm.nih.gov/faq#collection), which is the image set used in the cited paper. Thus, this automatic classifier can be used to label all of these images so that the medical software relying on these DICOM tags can perform their duty.
 
Another purpose of implementing this paper was to get experience with and learn about a wide range of technologies. Using this paper's algorithm as the core of the application, I utilized the following technologies to build the application:
 - PostgreSQL to organize the metadata of all of the downloaded images
 - QT to provide a simple multi-threaded user interface
 - Various imaging technologies (see *Notable Python libraries used* section) for implementing the algorithm itself
 - PyInstaller for packaging the application into an executable
 - VMware for testing
 - Proper logging using Python's built-in logging library
 - Git: Large File Storage, Submodules

## Data
As stated, I used the same data set that was in the paper ([NLM Image Set](https://openi.nlm.nih.gov/faq#collection)). This consists of 7470 chest X-ray images (CR) in the form of DICOM images. To organize the image set, I stored the metadata from the DICOM images into a PostgreSQL database using my [DicomToDatabase repository](https://github.com/Matt-Conrad/DicomToDatabase) I made. 

While this app can handle processing of all 7470 images, I also provide a subset (10 images) of the dataset in the *NLMCXR_subset_dataset.tgz*. Altogether, the entire NLM image set is 117.4GB unpacked and 80.7GB packed, so the subset is preferrable. Currently the code is set up to operate with the subset. If you would like to switch to the full image set, you must go into the *main.py* file and uncomment line 33 and comment line 34.

## Performance
Using the horizontal and vertical profile method from the paper, I am able to get an accuracy of 98.4% with the complete NLM image set, which is the same reported in the paper. Additionally, I am able to get the 90% accuracy when using the body-size ratio method, however I do not use it at the core of this application as it is much lower accuracy. 

## Testing
Workflow testing of the app and executables was done on the following environments:
   - Windows 10 laptop with Intel i7-4700MQ CPU and NVIDIA GeForce GT 755M GPU (Only source code testing done)
   - Fresh Ubuntu 18.04 virtual machine using VMware Workstation Player 15 on top of an Ubuntu 18.04 Desktop with AMD Ryzen 2600 CPU and NVIDIA RTX 2070 Super GPU

## Notable Python libraries used
 - psycopg2 for working with PostgreSQL
 - numpy for most calculations
 - scipy, scikit-image for feature calculation
 - pydicom for working with DICOM files
 - opencv for image preprocessing
 - pyqt5 for GUI development and multi-threading
 - pyinstaller for packaging application

## Usage
There are several usage paths that one can use. I will be providing the source code, a way to compile a folder-based executable, and a single executable. NOTE: According to PyInstaller, since I compiled these executables on Ubuntu 18.04 only Linux users can execute the executables. I will need to compile the source code on other OSs to provide those executables. 
 
 ### Using source code
 Here are the steps for using the app from the source code:
 1. Clone the git repository onto your computer (note this Git repository has 2 Git submodules so we need to take that into account): 
    ```
    git clone --recurse-submodules -j8 https://github.com/Matt-Conrad/CXR_View_Classification.git
    ```
 2. If you don't already have it, install anaconda using [these instructions](https://docs.anaconda.com/anaconda/install/)
 3. Run the following commands to build and enter the conda environment. Note: The environment.yml has *nomkl* library in it, which I needed for my AMD-based computer. If you're on Windows, you may need to remove that library to get this environment installed: 
    ```
    conda env create -f environment.yml
    conda activate cxr_view_env
    ```
 4. If you don't already have it, install PostgreSQL using [these instructions](https://wiki.postgresql.org/wiki/Detailed_installation_guides). If you're on Ubuntu, I used the following to get PostgreSQL set up:
    1. Create the following file: /etc/apt/sources.list.d/pgdg.list
    2. Add the following line to the file: ```http://apt.postgresql.org/pub/repos/apt/ bionic-pgdg main```. Alternatively, you could replace the *bionic-pgdg* (for Ubuntu 18.04) with *xenial-pgdg* (for Ubuntu 16.04).
    3. Run the following commands:
    ```
    sudo apt-get update
    sudo apt-get install postgresql-12
    ```
    4. Now that you have postgresql installed. Start the DB cluster with:
    ```
    sudo systemctl start postgresql@12-main
    ```
    5. Maybe unnecessary, but I set the password for the *postgres* user with:
    ```
    sudo -u postgres -i
    psql
    \password postgres
    ```
    Confirm the password, and now you have a working version of PostgreSQL on your computer.
 5. The last step before running the application is to optionally change the settings of the config.ini file
    1. (OPTIONAL) Change the default configuration if you wish. \
      - The *postgresql* section contains the server host and port, desired name of the DB to be created, as well as user and password. The template is currently set up to create a DB named "db" on the localhost, so you can leave it as is or rename it if you wish. 
      - Leave the *dicom_folder* section alone as it gets filled in automatically as the app goes through the steps. You can also rename the tables that will be created.
      - You can leave the *table_info* section alone, or if you want to change the names of the tables you can here
      - Feel free to leave the *logging* section alone. For more detail, go down to the *Logging* section of this README
      - Currently the code is set up to operate with the subset. If you would like to switch to the full image set, you must change the *dataset_info* section to either be "full_set" or "subset"
 6. If you are trying to use the dataset subset then you must delete the *NLMCXR_subset_dataset.tgz* from the cloned git repository since the TGZ comes with the code. In order to see the entire workflow, you must delete it from your local repository so that the GUI will start from the beginning of the process. 
 7. Run the app using the following command: ```python main.py```

 ### Using the folder-based executable
 This executable was created with PyInstaller by providing my *folder.spec* file in the following command: ```pyinstaller folder.spec```. You can find the executable if you unpack the *dist_folder.zip* from the Github repository. Here are the steps for running it:
 1. Clone the *dist_folder.zip* folder from the Github repository and unzip it.
 2. If you don't already have it, install PostgreSQL by following the steps from step 4 of the above section (*Using source code*). 
 3. Change the *config.ini* file in the *dist_folder/main/* folder as explained step 5 from the above section
 4. Execute the *main* executable and go through the steps.

 ### Using the single-file executable
 This executable was created with PyInstaller by providing my *one_file.spec* file in the following command: ```pyinstaller one_file.spec```. You can find the executable if you unpack the *dist_one_file.zip* from the Github repository. Here are the steps for running it:
 1. Clone the *dist_one_file.zip* folder from the Github repository and unzip it.
 2. If you don't already have it, install PostgreSQL by following the steps from step 4 of the source code section (*Using source code*). 
 3. Change the *config.ini* file in the *dist_one_file* folder as explained step 5 from the source code section
 4. Execute the *main* executable and go through the steps.

## Troubleshooting
 ### Logs
 When the source code or executables are run, they produce a log called the *CXR_Classification.log*. This log contains messages that alert the user of where it is at in the code. The *config.ini* file contains the setting, *level*, under the *logging* section for the level of logging the user would like to see in the log. Currently, this can be set to "info" or "debug". The default for this setting is "info".

 ### Known issues
 - The only error that I get is occasionally the below error. This error shows up in the terminal at the end of the stages sometimes. I am currently troubleshooting the cause.
 ```
 QBasicTimer::stop: Failed. Possibly trying to stop from a different thread.
 ```

## Future work
Ideas for future improvements:
 - Implement underlying algorithm as a web service so that users can pass any chest X-ray to the service
 - Fix bugs in one of the PHOG algorithm define in the paper to improve accuracy
 - Use C++ for the algorithm to boost speed
 - Provide option to import image labels instead of labeling manually (I implemented the manual labeling because this dataset did not come with labels, so I manually labeled the dataset using this sub-app)
 - Add executables for other OSs
 - Make it so that nomkl only installs if you have AMD processor
 - Convert the Git submodules to Python packages
 - Use pytest for unit testing
 - Make image set source URL more visible to user