pipeline {
    agent any
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

        // stage('Build Python folder implementation') {
        //     steps {
        //         dir('./miscellaneous') {
        //             sh "chmod u+x ./pyinstallerSetup.sh"
        //             sh "sudo ./pyinstallerSetup.sh" // Must give user execute sudo permission for this folder in sudoers
        //         }

        //         // Folder version
        //         dir('./Python/pyinstaller') {
        //             sh '../../miscellaneous/CXR_env/bin/pyinstaller folder.spec'
        //         }
        //         dir('./Python/builds') {
        //             sh 'zip -r dist_folder.zip dist_folder'
        //         }

        //         // File version
        //         dir('./Python/pyinstaller') {
        //             sh '../../miscellaneous/CXR_env/bin/pyinstaller one_file.spec'
        //         }
        //         dir('./Python/builds') {
        //             sh 'zip -r dist_one_file.zip dist_one_file'
        //         }
        //     }
        // }

        // stage('Build C++ implementation') {
        //     steps {
        //         // must run cppSetup.sh first
        //         sh 'mkdir ./Cpp/build'
        //         dir('./Cpp/build') {
        //             sh 'qmake ../CXR_classify/CXR_classify.pro CONFIG+=debug'
        //             sh 'make -j4'
        //         }
        //         dir('./Cpp') {
        //             sh 'zip -r cppBuild.zip build'
        //         }           
        //     }
        // }

        // stage('Build shared libraries') {
        //     steps {
        //         sh 'chmod u+x ./miscellaneous/combinedCmakeBuild.sh'
        //         sh './miscellaneous/combinedCmakeBuild.sh'
        //         dir('./Combined/DesktopApp/build') {
        //             sh 'zip -r combinedSharedLibraries.zip build'
        //         }
        //     }
        // }

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
                sh "chmod u+x ./miscellaneous/installation.sh"
                sh "./miscellaneous/installation.sh"
            }
        }
    }
}