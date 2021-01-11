# Implementation of Chest X-ray Image View Classification
This project is an implementation of the paper "Chest X-ray Image View Classification" by Xue et al found [here](https://www.researchgate.net/publication/283778178_Chest_X-ray_Image_View_Classification). Currently, the project is split into 2 parts: a desktop application for training the algorithm and a web API for deploying the trained algorithm. 

The desktop app is a Qt GUI application that guides the user through the training steps including: downloading the image set, unpacking it, storing the metadata, extracting the features, data labaling, cross-validation, and classifier training. The application is optimally coded in C++, Python, and a combined Python/C++ solution. All implementations come with full logging and the Python implementation is equipped with a suite of pytest unit tests. 

The web API contains the trained model and I outline steps below on how to deploy either to the local machine, a local VM, or to AWS Elastic Beanstalk.  

## Motivation
The inspiration for this project arises from my experience in the medical imaging industry. A classifier such as this would be useful in industry. One use case being a lot of medical imaging software relies on DICOM tags such as laterality (0020,0060), view position (0018,5101), and patient orientation (0020,0020) to perform some action. However, this tag is not always there or has values of all images in the study or series as seen in the image set from [NLM History of Medicine](https://openi.nlm.nih.gov/faq#collection), which is the image set used in the cited paper. Thus, this automatic classifier can be used to label all of these images so that the medical software relying on these DICOM tags can perform their duty.
 
The main purpose of this project was to learn about a wide range of technologies and concepts by combining them into one large project. Using this paper's algorithm as the core of the project, I utilized the following technologies and concepts to build the application and web API:
 - PostgreSQL (Python package: psycopg2, C++ library: libpqxx) to organize the metadata, features, and labels of all of the downloaded images
 - Qt for building multi-threaded
 - NumPy for most calculations in Python
 - Pydicom Python library and DCMTK C++ library for working with DICOM files
 - Flask for designing the web API and web app
 - Amazon Web Services (AWS) Elastic Beanstalk for deploying the Flask app to the cloud
 - Gunicorn and Nginx to securely deploy the Flask app web API to a local virtual machine
 - OpenCV for image processing in both Python and C++
 - pytest for writing an automated suite of unit tests
 - Boost for configuration file handling in C++
 - Armadillo for matrix operations in C++
 - mlpack for dataset manipulation and machine learning in C++
 - Object-Oriented Concepts: Inheritance (including multiple), Encapsulation, Polymorphism, Abstraction, Coupling & Cohesion
 - ctypes Python library for wrapping C++ functionality
 - UML class diagram for modeling system
 - PyInstaller for building Python implementation into an executable
 - g++, Make, QMake, and CMake build tools for building C++ executables and shared libraries
 - VMware Workstation for testing on local virtual machines
 - Proper logging using Python's built-in logging library and spdlog C++ library
 - Git: Large File Storage, Submodules
 - Python packaging and deployment to PyPI
 - Multi-threading using QThreadPool and the standard thread library
 - Downloading dataset: Qt for C++ and requests library for Python
 - Github Issues for bug and task tracking
 - Jenkins for CI/CD
 - Shell scripting (Bash)

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
   - Fresh Ubuntu 20.04 virtual machine using VMware Workstation Player 16 on top of an Ubuntu 20.04 Laptop with AMD 3rd Generation Ryzen 9 4900HS and NVIDIA GeForce RTX 2060 Max-Q

## Desktop App Usage
Since there are 3 implementations of the app, there are many ways to build and run it:
- Python implementation
   1. Run source code
   2. Run pre-built file-based executable
   3. Run pre-built folder-based executable
   4. Build and run file-based executable
   5. Build and run folder-based executable
- C++ implementation
   1. Run pre-built executable
   2. Build using QMake and run the resulting executable
- Combined implementation
   1. Run Python source code with pre-built C++ shared libraries
   2. Build C++ side using individual g++ commands and run Python source code
   3. Build C++ side using provided Makefile and run Python source code
   4. Build C++ side using CMake and run Python source code

NOTE: Pre-built executables and shared libraries are compiled on Ubuntu 20.04 so they may only work on that OS. Additionally, scripts for building are targeted toward Ubuntu/Linux users.

 ### For all paths
 1. Clone the git repository onto your computer: 
    ```
    git clone https://github.com/Matt-Conrad/CXR_View_Classification.git
    ```
 2. Set up Postgres if you don't already have it by running postgresSetup.sh in miscellaneous folder: ```./postgresSetup.sh```
 2. (OPTIONAL) Change the default configuration if you wish. 
      - The *postgresql* section contains the server host and port, desired name of the DB to be created, as well as user and password. The template is currently set up to create a DB named "db" on the localhost, so you can leave it as is or rename it if you wish. 
      - Leave the *dicom_folder* section alone as it gets filled in automatically as the app goes through the steps. You can also rename the tables that will be created.
      - You can leave the *table_info* section alone, or if you want to change the names of the tables you can here
      - Feel free to leave the *logging* section alone. For more detail, go down to the *Logging* section of this README
      - Currently the code is set up to operate with the subset. If you would like to switch to the full image set, you must change the *dataset_info* section to either be "full_set" or "subset"

 ### Python
 Here are the steps for using the app for the various paths.

 #### Running from source and building 
 1. Run pythonSetup.sh file in *miscellaneous* folder to set up Python: ```./pythonSetup.sh [arg]```
   - ```./pythonSetup.sh source``` if you're going to run from source
   - ```./pythonSetup.sh build``` if you're going to build the file-based or folder-based executable
 2. Activate the virtualenv: ```source CXR_env/bin/activate```
 3. (Optional) If you're going to build the executable, run ```pyinstaller [arg]``` in *CXR_View_Classification/Python/pyinstaller*
   - ```pyinstaller folder.spec``` if building folder-based executable
   - ```pyinstaller one_file.spec``` if building file-based executable
 4. Run the program:
   - ```python main.py``` in *CXR_View_Classification/Python/DesktopApp* if you're running from source
   - ```./CXR_Classify``` *CXR_View_Classification/Python/builds/dist_folder* executable for folder-based approach
   - ```./CXR_Classify``` *CXR_View_Classification/Python/builds/dist_one_file* executable for file-based approach

 #### Run pre-built folder-based and file-based executables
 1. Download and unzip the *FOLDER_NAME.zip* from the Github release
 2. Execute the *CXR_Classify* executable in *FOLDER_NAME* folder
   - Where FOLDER_NAME is *dist_folder* if using the folder-based executable and *dist_one_file* if using the file-based executable

 ### C++ Implementation

 #### Run pre-built executable
 1. Run the cppSetup.sh script to set up C++ libraries: ```./cppSetup.sh prebuilt```
 2. Download the *cppBuild.zip* folder from the Github release and unzip it.
 3. Execute the provided executable and go through the steps.

 #### Build using QMake and run the resulting executable
 1. From miscellaneous folder, run cppSetup.sh to set up C++ libraries: ```./cppSetup.sh build```
 2. Build executable using qmake:
   - Create and change to build directory: cd ```mkdir ../Cpp/build && cd ../Cpp/build```
   - Create build system using qmake: ```qmake ../CXR_classify/CXR_classify.pro CONFIG+=debug```
   - Build the executable: ```make```
 3. Execute the *CXR_View_Classification/Cpp/build/CXR_classify* executable and go through the steps.

 ### Combined Implementation
 The source code for this implementation can be found in *CXR_View_Classification/Combined/DesktopApp/src*. Along with the source code, there is also a Makefile and a CMakeList.txt file in there to aid building the executables. There are 3 equivalent ways to build this code: g++ commands, Make, and CMake. 
 1. From the miscellaneous folder, run the build script with the desired argument to set up and build the shared libraries: ```./combinedBuild.sh [arg]```
   - ```./combinedBuild.sh download``` if you're going to download the shared libraries
   - ```./combinedBuild.sh g++``` if you're going to build using the g++ method
   - ```./combinedBuild.sh make``` if you're going to build using the Make method
   - ```./combinedBuild.sh cmake``` if you're going to build using the CMake method
 2. (Optional) If you're going the download route, then download the *combinedSharedLibraries.zip* folder from the Github release and unzip it.
 3. Activate the virtualenv: ```source CXR_env/bin/activate```
 4. (Optional) If you're doing the download route, add the Qt lib to LD_LIBRARY_PATH so program can find Qt shared: ```export LD_LIBRARY_PATH="/PATH/TO/CXR_env/lib/python3.6/site-packages/PyQt5/Qt/lib:$PATH"```
 5. Run the app using Python: ```cd ../Combined/DesktopApp && python main.py```


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

