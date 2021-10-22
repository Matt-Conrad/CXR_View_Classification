How to build this app:

- Follow [this](https://github.com/therecipe/qt/wiki/Installation-on-Linux) guide and install the required packages:

sudo apt-get -y install build-essential libglu1-mesa-dev libpulse-dev libglib2.0-dev

and in the "If you just want to compile an application" section there's a command for installing in the module. For now that's what I'll use.

- Run this command to get the QT Golang library in the current folder which should be CXR_View_Classification/Go/CxrClassify:

export GO111MODULE=on; go install -v -tags=no_env github.com/therecipe/qt/cmd/... && go mod vendor && git clone https://github.com/therecipe/env_linux_amd64_513.git vendor/github.com/therecipe/env_linux_amd64_513

export GO111MODULE=on; git clone https://github.com/therecipe/examples.git && cd ./examples && go install -v -tags=no_env github.com/therecipe/qt/cmd/... && go mod vendor && git clone https://github.com/therecipe/env_linux_amd64_513.git vendor/github.com/therecipe/env_linux_amd64_513 && $(go env GOPATH)/bin/qtdeploy test desktop ./basic/widgets


If there are issues with vendor, it might be good to delete vendor and rerun the above line

- Note: It may be required to run "go mod init" and then maybe "go mod tidy" to set up the go.mod and go.sum that details the CxrClassify

From here, you should be able to build using:

$(go env GOPATH)/bin/qtdeploy test desktop CxrClassify

or if you just want the executable, then "build" instead of "test"

The set up instructions will be solidified after more repetitions during CI



# THIS IS WHAT WORKED
go mod init CxrClassify

export GO111MODULE=on; go install -v -tags=no_env github.com/therecipe/qt/cmd/... && go mod vendor

$(go env GOPATH)/bin/qtdeploy build desktop CxrClassify

go mod tidy

$(go env GOPATH)/bin/qtdeploy build desktop CxrClassify

go mod vendor

$(go env GOPATH)/bin/qtdeploy build desktop CxrClassify

git clone https://github.com/therecipe/env_linux_amd64_513.git vendor/github.com/therecipe/env_linux_amd64_513

$(go env GOPATH)/bin/qtdeploy build desktop CxrClassify


# If you're adding a package in the future do a go mod vendor to add it to vendor folder, it seems  like you have to run the git clone command afterwards too
