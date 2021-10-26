How to build this app:

- Follow [this](https://github.com/therecipe/qt/wiki/Installation-on-Linux) guide and install the required packages:

sudo apt-get -y install build-essential libglu1-mesa-dev libpulse-dev libglib2.0-dev

and in the "If you just want to compile an application" section there's a command for installing in the module. For now that's what I'll use.


# THIS IS WHAT WORKED
go mod init CxrClassify

go mod vendor

$(go env GOPATH)/bin/qtdeploy build desktop CxrClassify

go mod vendor

git clone https://github.com/therecipe/env_linux_amd64_513.git vendor/github.com/therecipe/env_linux_amd64_513

$(go env GOPATH)/bin/qtdeploy test desktop CxrClassify


# NOTES:
- If you're adding a package in the future do a go mod vendor to add it to vendor folder, it seems  like you have to run the git clone command afterwards too
- Once the environment is set up, you can run "rm */moc*" to remove all moc related stuff without ruining the environment
- Classes can't have the same first x number of letters in its name otherwise there's collision during compilation of the qtdeploy build which seems to be a non-documented limitation
