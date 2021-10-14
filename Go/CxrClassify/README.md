How to build this app:

- Follow [this](https://github.com/therecipe/qt/wiki/Installation-on-Linux) guide and install the required packages:

sudo apt-get -y install build-essential libglu1-mesa-dev libpulse-dev libglib2.0-dev

and in the "If you just want to compile an application" section there's a command for installing in the module. For now that's what I'll use.

- Run this command to get the QT Golang library in the current folder which should be CXR_View_Classification/Go/CxrClassify:

export GO111MODULE=on; go install -v -tags=no_env github.com/therecipe/qt/cmd/... && go mod vendor && git clone https://github.com/therecipe/env_linux_amd64_513.git vendor/github.com/therecipe/env_linux_amd64_513

- Note: It may be required to run "go mod init" and then maybe "go mod tidy" to set up the go.mod and go.sum that details the CxrClassify

From here, you should be able to build using:

$(go env GOPATH)/bin/qtdeploy test desktop CxrClassify

or if you just want the executable, then "build" instead of "test"

The set up instructions will be solidified after more repetitions during CI