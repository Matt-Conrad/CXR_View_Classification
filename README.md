# Chest X-ray Image View Classification
The heart of this project is an image classifier based on [this paper](https://www.researchgate.net/publication/283778178_Chest_X-ray_Image_View_Classification) that can determine whether a Chest X-ray is a frontal or lateral view orientation. Additionally, there are a bunch of other technologies built around this core algorithm to facilitate use of the classifier. 

The project can be split into 2 parts: a desktop application for training the algorithm and a deployable web API with an accompanying web UI for utilizing the trained algorithm. 

The desktop app is a Qt GUI application that guides the user through the training steps including: downloading the image set, unpacking it, storing the metadata, extracting the features, data labaling, cross-validation, and classifier training. The application is optimally coded in C++, Python, and a combined Python/C++ solution. All implementations come with full logging and the Python implementation is equipped with a suite of pytest unit tests. 

The web API contains the trained model and accepts DICOM files to classify as either frontal or lateral and can be deployed either to the local machine, a local VM, or to AWS Elastic Beanstalk. The web API can be easily used with the complementary web UI. 

## Motivation
Medical images in the form of DICOM files can have tags such as laterality (0020,0060), view position (0018,5101), and patient orientation (0020,0020) that describe the orientation of a patient. However, this tag is not always there or this tag can have incorrect values. Examples of these issues can be seen in the image set from [NLM History of Medicine](https://openi.nlm.nih.gov/faq#collection), which is the image set used in the cited paper. Thus, this automatic classifier can be used to label all of these images.
 
The main purpose of this project was to learn about a wide range of technologies and concepts and how to integrate them into one large project. Using this paper's algorithm as the core of the project, I utilized the following technologies and concepts to build the application and web API:
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
 - HTML, CSS, JavaScript for web UI using bootstrap, cornerstone, and AJAX technologies

## Data
As stated, I used the same data set that was in the paper ([NLM Image Set](https://openi.nlm.nih.gov/faq#collection)). This consists of 7470 chest X-ray images (CR) in the form of DICOM images. To organize the image set, I stored the metadata from the DICOM images into a PostgreSQL database using my [DicomToDatabase repository](https://github.com/Matt-Conrad/DicomToDatabase) I made. 

While the training app can handle processing of all 7470 images, I also provide a subset (10 images) of the dataset in the *NLMCXR_subset_dataset.tgz* to test the app and to make it quicker to go through the steps of the app. The model trained with all 7470 images using the app is also included as *full_set_classifier.joblib*. Altogether, the entire NLM image set is 117.4GB unpacked and 80.7GB packed, so the subset is preferrable. Currently the code is set up to operate with the subset. If you would like to switch to the full image set, you must go into the *config.ini* file and set ```dataset=full_set``` in the *dataset_info* section.

## Performance
Using the horizontal and vertical profile method from the paper, I am able to get an accuracy of 98.4% while using 2/3 of the NLM image set as the training set with 10-fold cross-validation, which is the same reported in the paper. Additionally, I am able to get the 90% accuracy when using the body-size ratio method, however I do not use it at the core of this application as it is a much lower accuracy. For the profile method, I also get a 98.4% with the test set.

<img src="miscellaneous/images/Performance.png" alt="drawing" width="750"/>

As one would expect, the C++ implementation is faster than the Python approach, and the Combined implementation performs on par with the C++ one. This Combined approach has the best of both worlds: the quick development of Python code and the speedy execution of C++ for performance critical areas. This exercise is a testament that using both Python and C++ in development is an impactful combination.   

## Testing
The suite of unit tests were created using Pytest and can be found in Python > DesktopApp > test. These tests mainly cover the backend functionality of the app such as downloading and feature calculation. To run the tests, the pip environment must be set up (see section *Using source code* on how to set that up). Once done, all you have to do is run ```pytest .``` from the test folder.

Workflow testing of the app and executables was done on the following environments:
   - Windows 10 laptop with AMD 3rd Generation Ryzen 9 4900HS and NVIDIA GeForce RTX 2060 Max-Q (Only source code testing done)
   - Fresh Ubuntu 18.04 virtual machine using VMware Workstation Player 15 on top of an Ubuntu 18.04 Desktop with AMD Ryzen 2600 CPU and NVIDIA RTX 2070 Super GPU
   - AWS Elastic Beanstalk web server on a Python 3.6 platform running on 64-bit Amazon Linux
   - Fresh Ubuntu 20.04 virtual machine using VMware Workstation Player 16 on top of an Ubuntu 20.04 Laptop with AMD 3rd Generation Ryzen 9 4900HS and NVIDIA GeForce RTX 2060 Max-Q

## Desktop App Usage
![](miscellaneous/images/DesktopApp.png)

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

You can find the steps for each in the [wiki](https://github.com/Matt-Conrad/CXR_View_Classification/wiki/Desktop-App-Usage-Steps).

NOTE: Pre-built executables and shared libraries are compiled on Ubuntu 20.04 so they may only work on that OS. Additionally, scripts for building are targeted toward Ubuntu/Linux users.

## Web API/UI Usage for local machine or local VM and AWS Elastic Beanstalk
<img src="miscellaneous/images/WebUI.png" alt="drawing" width="650"/>

There are several ways to deploy the web interfaces: standalone built-in Flask server, standalone Gunicorn server running the Flask app, and an Nginx/Gunicorn server pair where the Nginx server works as a reverse proxy for the Gunicorn server running Flask (recommended).

The steps for deploying the model from source code can be found in the the [wiki](https://github.com/Matt-Conrad/CXR_View_Classification/wiki/Web-API-UI-Usage-Steps).

