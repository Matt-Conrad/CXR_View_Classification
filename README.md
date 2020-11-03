# Implementation of Chest X-ray Image View Classification
This project is an implementation of the paper "Chest X-ray Image View Classification" by Xue et al found [here](https://www.researchgate.net/publication/283778178_Chest_X-ray_Image_View_Classification). Currently, the implementation is in the form of a desktop application coded in both Python and C++, as well as a web API in Python. 

The desktop app is a Qt application that allows a user to interact with a GUI to go through the all of the steps including: downloading, storing metadata, extracting features, data labaling, cross-validation, and classifier training. The application is available and optimized in C++, Python, and a Combined solution. All implementations come with full logging and the Python implementation is equipped with a suite of pytest unit tests. 

The web API is a RESTful web API and contains the trained model and I outline steps below on how to deploy either to the local machine, a local VM, or to AWS Elastic Beanstalk.  

## Motivation
The inspiration for this project arises from my experience in the medical imaging industry. A classifier such as this would be useful in industry. One use case being a lot of medical imaging software relies on DICOM tags such as laterality (0020,0060), view position (0018,5101), and patient orientation (0020,0020) to perform some action. However, this tag is not always there or has values of all images in the study or series as seen in the image set from [NLM History of Medicine](https://openi.nlm.nih.gov/faq#collection), which is the image set used in the cited paper. Thus, this automatic classifier can be used to label all of these images so that the medical software relying on these DICOM tags can perform their duty.
 
The main purpose of implementing this paper was to get experience with and learn about a wide range of technologies and concepts. Using this paper's algorithm as the core of the project, I utilized the following technologies and concepts to build the application and web API:
 - PostgreSQL (Python package: psycopg2, C++ library: libpqxx) to organize the metadata, features, and labels of all of the downloaded images
 - Qt to provide a simple multi-threaded user interface for guiding the user from image set download to classifier training
 - NumPy for most calculations in Python
 - SciPy, scikit-image for feature calculation
 - Pydicom Python library and DCMTK C++ library for working with DICOM files
 - Flask for designing the web API and web app
 - Amazon Web Services (AWS) Elastic Beanstalk for deploying the Flask app to the cloud
 - Gunicorn, and Nginx to deploy the Flask app as a RESTful web API to a local virtual machine
 - OpenCV for image preprocessing in both Python and C++
 - pytest for writing an automated suite of unit tests
 - Boost for configuration file handling in C++
 - Armadillo for matrix operations in C++
 - mlpack for machine learning in C++
 - OO Concept: Inheritance (including multiple)
 - ctypes Python library for wrapping C++ functionality
 - UML class diagram for modeling system
 - PyInstaller for packaging the application into an executable
 - VMware for testing on local virtual machines
 - Proper logging using Python's built-in logging library and spdlog C++ library
 - Git: Large File Storage, Submodules
 - Python packaging and deployment to PyPI
 - g++, Make, QMake, and CMake build tools

## Data
As stated, I used the same data set that was in the paper ([NLM Image Set](https://openi.nlm.nih.gov/faq#collection)). This consists of 7470 chest X-ray images (CR) in the form of DICOM images. To organize the image set, I stored the metadata from the DICOM images into a PostgreSQL database using my [DicomToDatabase repository](https://github.com/Matt-Conrad/DicomToDatabase) I made. 

While the training app can handle processing of all 7470 images, I also provide a subset (10 images) of the dataset in the *NLMCXR_subset_dataset.tgz* to test the app and to make it quicker to go through the steps of the app. The model trained with all 7470 images using the app is also included as *full_set_classifier.joblib*. Altogether, the entire NLM image set is 117.4GB unpacked and 80.7GB packed, so the subset is preferrable. Currently the code is set up to operate with the subset. If you would like to switch to the full image set, you must go into the *config.ini* file and set ```dataset=full_set``` in the *dataset_info* section.

## Performance
Using the horizontal and vertical profile method from the paper, I am able to get an accuracy of 98.4% while using 2/3 of the NLM image set as the training set with 10-fold cross-validation, which is the same reported in the paper. Additionally, I am able to get the 90% accuracy when using the body-size ratio method, however I do not use it at the core of this application as it is a much lower accuracy. For the profile method, I also get a 98.4% with the test set.

TODO Add speed performance statistics

## Testing
The suite of unit tests were created using Pytest and can be found in Python > DesktopApp > test. These tests mainly cover the backend functionality of the app such as downloading and feature calculation. To run the tests, the pip environment must be set up (see section *Using source code* on how to set that up). Once done, all you have to do is run ```pytest .``` from the test folder.

Workflow testing of the app and executables was done on the following environments:
   - Windows 10 laptop with Intel i7-4700MQ CPU and NVIDIA GeForce GT 755M GPU (Only source code testing done)
   - Fresh Ubuntu 18.04 virtual machine using VMware Workstation Player 15 on top of an Ubuntu 18.04 Desktop with AMD Ryzen 2600 CPU and NVIDIA RTX 2070 Super GPU
   - AWS Elastic Beanstalk web server on a Python 3.6 platform running on 64-bit Amazon Linux

## Desktop App Usage
There are several usage paths that one can use. I will be providing the source code, a way to compile a folder-based executable, and a single executable. NOTE: According to PyInstaller, since I compiled these executables on Ubuntu 18.04 only Linux users can execute the executables. I will need to compile the source code on other OSs to provide those executables. 
 
 ### Using source code
 Here are the steps for using the app from the source code:
 1. Clone the git repository onto your computer: 
    ```
    git clone https://github.com/Matt-Conrad/CXR_View_Classification.git
    ```
 2. If you don't already have it, install pip using [these instructions](https://pip.pypa.io/en/stable/installing/)
 3. Install virtualenv and Python 3.6 if you don't already have it. You can install virtualenv using [these instructions](https://virtualenv.pypa.io/en/latest/installation.html). Create a virtualenv using ```virtualenv -p PATH_TO_PYTHON_3.6 CXR_env``` to create a folder containing virtual environment files. Activate the environment using ```source CXR_env/bin/activate```. Lastly, install the pip packages using ```pip install -r requirements.txt``` from inside the *miscellaneous* folder.
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
 This executable was created with PyInstaller by providing my *folder.spec* file in the following command: ```pyinstaller folder.spec```, you will need to run this command in the *CXR_View_Classification/Python/DesktopApp/pyinstaller* folder if you want to create it yourself. You can find the executable if you unpack the *dist_folder.zip* from the v1.0.0 release attachment in the Github repository. Here are the steps for running it:
 1. Download the *dist_folder.zip* folder from the Github release and unzip it.
 2. If you don't already have it, install PostgreSQL by following the steps from step 4 of the above section (*Using source code*). 
 3. Change the *config.ini* file in the *dist_folder/main/* folder as explained step 5 from the above section
 4. Execute the *main* executable and go through the steps.

 ### Using the single-file executable
 This executable was created with PyInstaller by providing my *one_file.spec* file in the following command: ```pyinstaller one_file.spec```, you will need to run this command in the *CXR_View_Classification/Python/DesktopApp/pyinstaller* folder if you want to create it yourself. You can find the executable if you unpack the *dist_folder.zip* from the v1.0.0 release attachment in the Github repository. Here are the steps for running it:
 1. Download the *dist_one_file.zip* folder from the Github repository and unzip it.
 2. If you don't already have it, install PostgreSQL by following the steps from step 4 of the source code section (*Using source code*). 
 3. Change the *config.ini* file in the *dist_one_file/* folder as explained step 5 from the source code section
 4. Execute the *main* executable and go through the steps.

## Web API Usage for local machine or local VM
There are several ways to deploy the web interfaces: standalone built-in Flask server, standalone Gunicorn server running the Flask app, and an Nginx/Gunicorn server pair where the Nginx server works as a reverse proxy for the Gunicorn server running Flask (recommended). Below I discuss the preparation required for each path, then I provide the following instructions

 ### Preparation for all ways
 Here are the steps for deploying the model from the source code:
 1. Clone the git repository onto your computer: 
    ```
    git clone https://github.com/Matt-Conrad/CXR_View_Classification.git
    ```
 2. If you don't already have it, install pip using [these instructions](https://pip.pypa.io/en/stable/installing/)
 3. Install virtualenv and Python 3.6 if you don't already have it. You can install virtualenv using [these instructions](https://virtualenv.pypa.io/en/latest/installation.html). Create a virtualenv using ```virtualenv -p PATH_TO_PYTHON_3.6 CXR_env``` to create a folder containing virtual environment files. Activate the environment using ```source CXR_env/bin/activate```. Lastly, install the pip packages using ```pip install -r requirements.txt``` from inside the *miscellaneous* folder.

 ### Standalone Built-in Flask Server
 4. Open a terminal in the cloned repository and run the following command to add/update the following OS (in this case Linux) environment variables. Note: If you are on Windows, you need to replace the "export" keyword with "set":
    ```
    export FLASK_APP=api_controller
    ```
 5. To run the server so that only the host computer has access to it, use the following command: ```flask run```. To run the server so that other computers on the local network have access, use the following command: ```flask run --host=0.0.0.0```
 6. You now have a running standalone built-in Flask server. Use the send_script.py script to send a DCM file over HTTP to port **5000** on the localhost (127.0.0.1) if you didn't provide the *host* parameter in step 5, the IP address of the host if you did provide *host*. Note: This is a development server and is not recommended to be used as a production server.

 ### Standalone Gunicorn Server Running The Flask App:
 4. Open a terminal in the cloned repository and run the following command: ```gunicorn api_controller:app```.
 5. You now have a running standalone Gunicorn server running the Flask app. Use the send_script.py script to send a DCM file over HTTP to port **8000** on the localhost (127.0.0.1). Note: Since Gunicorn is easily susceptible to DOS attacks, it is recommended to run Gunicorn behind a reverse proxy server which is why I only instruct to send to the localhost here. 

 ### Nginx/Gunicorn server pair (Recommended)
 4. Open a terminal in the cloned repository and run the following command to run Flask app on the Gunicorn server in the background as a daemon: ```gunicorn -D api_controller:app```.
 5. Now we need to set up the Nginx server If you don't already have Nginx, install it with the following commands:
    ```
    sudo apt-get update
    sudo apt-get install nginx
    ```
 6. Remove the file ```/etc/nginx/sites-available/default``` and replace it with a file named the exact same, but with the following content:
    ```
    server {
       listen 80;
       server_name cxr_classifier;
       access_log  /var/log/nginx/cxr_classifier.log;

       location / {
          proxy_pass http://127.0.0.1:8000;
          proxy_set_header Host $host;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       }
    }
    ```
 7. In order to send a DICOM file (which is about 10MB) over HTTP, we need to remove Nginx's request size cap. Add the following entry to the ```http``` section of the ```/etc/nginx/nginx.conf``` file:
    ```
    client_max_body_size 0;
    ```
 8. Start and then restart Nginx server:
    ```
    sudo service nginx start
    sudo service nginx restart
    ```
 9. You now have a running Nginx/Gunicorn server pair running the Flask app. In this setup, the Nginx server is operating on port **80** and accepts requests from the localhost or other computers on the network. The Nginx server will pass requests to the Gunicorn server on port **8000** of the same computer, but this Gunicorn server is not directly accessible to computers outside the localhost. Use the send_script.py script to send a DCM file over HTTP to port **80** of the target computer.  

## Web API Usage for AWS Elastic Beanstalk
 1. Clone the git repository onto your computer: 
    ```
    git clone https://github.com/Matt-Conrad/CXR_View_Classification.git
    ```
 2. Go to an AWS Elastic Beanstalk console > "Environments" Tab
 3. Click "Create a new environment", select "Web server environment". Enter an application name and environment name in their respective boxes.
 4. In the "Platform" section, select "Managed platform", set "Platform" = "Python", set "Platform branch" = "Python 3.6 running on 64-bit Amazon Linux", and set "Platform version" = "2.9.7"
 5. In the "Application code" section, select "Upload your code" and upload the */CXR_View_Classification/Python/Engine/aws_deploy/aws_deploy.zip* file. This zip contains all of the code from the *aws_deploy* folder.
 6. Select "Create environment" and wait for the environment to have Status: OK
 7. Copy the URL for the environment and open the *send_script.py* script. Uncomment line 38 and comment line 39. In line 38, paste the URL where the ```**ELASTIC_BEANSTALK_INSTANCE_URL**``` placeholder is. Make sure you have all or at least part of the *NLMCXR_dcm* folder (you can download it using the desktop app or directly from the website). Then run the script and it should send images over HTTP to the AWS EB instance

## Troubleshooting
 ### Logs
 - When the source code or executables are run, they produce a log called the *CXR_Classification.log*. This log contains messages that alert the user of where it is at in the code. The *config.ini* file contains the setting, *level*, under the *logging* section for the level of logging the user would like to see in the log. Currently, this can be set to "info" or "debug". The default for this setting is "info".
 - Additionally, the log for the Nginx engine is set for */var/log/nginx/cxr_classifier.log* in the */etc/nginx/sites-available/default* config file as specified in step 6 of *Nginx/Gunicorn server pair (Recommended)* above.

## Future work
Ideas for future improvements:
 - Provide an installer and configuration for the Gunicorn and Nginx server pair
 - Implement a HTML user interface for the web API
 - Add executables for other OSs
 - Make it so that nomkl only installs if you have AMD processor
 - Find a way to remove pre-installed Postgres dependency
 - Make image set source URL more visible to user
 - Fix bugs in one of the PHOG algorithm define in the paper to improve accuracy
 - Implement DICOM compliant HTTP transfer of DICOM files
 - Improve logging in AWS deployment
