#!/bin/bash
mkdir Combined/DesktopApp/build
cd Combined/DesktopApp/build
cmake ../src
cmake --build .