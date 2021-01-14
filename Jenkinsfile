pipeline {
    agent any
    parameters {
        booleanParam(name: 'buildPythonFileExecutableOnHost', defaultValue: false, description: 'Builds the Python file-based executable on host computer')
        booleanParam(name: 'buildPythonFolderExecutableOnHost', defaultValue: false, description: 'Builds the Python folder-based executable on host computer')
        booleanParam(name: 'buildCppExecutableOnHost', defaultValue: false, description: 'Builds the C++ executable on host computer')
        booleanParam(name: 'buildCombinedSharedLibsOnHost', defaultValue: false, description: "Builds Combined implementation's shared libs on host computer")
        booleanParam(name: 'setupPostgresOnGuest', defaultValue: false, description: 'Sets up PostgreSQL on the VM')
        booleanParam(name: 'setupPythonOnGuest', defaultValue: false, description: 'Sets up virtualenv on the VM for running Python implementation')
        booleanParam(name: 'setupCppOnGuest', defaultValue: false, description: 'Sets up C++ libraries on the VM for running C++ implementation')
        booleanParam(name: 'setupCombinedOnGuest', defaultValue: false, description: 'Sets up virtualenv and C++ libraries on the VM for running the Combined implementation')
        booleanParam(name: 'setupToBuildCppOnGuest', defaultValue: false, description: 'Sets up C++ libraries on the VM for building the C++ implementation')
        booleanParam(name: 'setupEngineOnGuest', defaultValue: false, description: 'Sets up the engine on the VM')
    }
    options {
        skipDefaultCheckout()
    }
    stages {
        stage('Prepare build folder') {
            steps {
                cleanWs()
            }
        }

        stage('Get source code') {
            steps {
                checkout scm
            }
        }

        stage('Build Python implementation') {
            stages {
                stage('Run pyinstaller setup on host machine') {
                    when {
                        anyOf {
                            expression { params.buildPythonFileExecutableOnHost == true }
                            expression { params.buildPythonFolderExecutableOnHost == true }
                        }
                    }
                    steps {
                        dir('./miscellaneous') {
                            sh "./pythonSetup.sh build" // Must give user execute sudo permission for this folder in sudoers
                        }
                    }
                }

                stage('Build file-based executable') {
                    when {
                        expression { params.buildPythonFileExecutableOnHost == true }
                    }
                    steps {
                        // File version
                        dir('./Python/pyinstaller') {
                            sh '../../miscellaneous/CXR_env/bin/pyinstaller one_file.spec'
                        }
                        dir('./Python/builds') {
                            sh 'zip -r dist_one_file.zip dist_one_file'
                        }
                    }
                }

                stage('Build folder-based executable') {
                    when {
                        expression { params.buildPythonFolderExecutableOnHost == true }
                    }
                    steps {
                        // Folder version
                        dir('./Python/pyinstaller') {
                            sh '../../miscellaneous/CXR_env/bin/pyinstaller folder.spec'
                        }
                        dir('./Python/builds') {
                            sh 'zip -r dist_folder.zip dist_folder'
                        }
                    }
                }
            }
        }

        stage('Build C++ implementation') {
            when {
                expression { params.buildCppExecutableOnHost == true }
            }
            steps {
                // sh "./miscellaneous/cppSetup.sh build"
                sh 'mkdir ./Cpp/build'
                dir('./Cpp/build') {
                    sh 'qmake ../CXR_classify/CXR_classify.pro CONFIG+=debug'
                    sh 'make -j4'
                }
                dir('./Cpp') {
                    sh 'zip -r cppBuild.zip build'
                }           
            }
        }

        stage('Build shared libraries') {
            when {
                expression { params.buildCombinedSharedLibsOnHost == true }
            }
            // environment {
            //     VM_UBUNTU_CREDS = credentials('vm-ubuntu-credentials')
            // }
            steps {                
                // dir('./miscellaneous') {
                //     sh "echo ${VM_UBUNTU_CREDS_PSW} | sudo -S ./combinedBuild.sh cmake"
                // }
                dir('./miscellaneous') {
                    sh './combinedBuild.sh cmake'  // Need to pass password without echoing to terminal somehow. This step makes it so we build but don't set up since missing password
                }
                dir('./Combined/DesktopApp') {
                    sh 'zip -r combinedSharedLibraries.zip build'
                }
            }
        }

        stage('Clean up') {
            steps {
                sh 'find . -name "*@tmp" -type d -delete'
            }
        }

        stage('Set up VM') {
            environment {
                VMREST_CREDS = credentials('vmrest-credentials-for-cxr-classify')
                VM_UBUNTU_CREDS = credentials('vm-ubuntu-credentials')
            }
            steps {
                sh "./miscellaneous/installation.sh $setupPostgresOnGuest $setupPythonOnGuest $setupCppOnGuest $setupCombinedOnGuest $setupToBuildCppOnGuest $setupEngineOnGuest"
            }
        }
    }
}