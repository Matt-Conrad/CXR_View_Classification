import sys
from PyQt5.QtWidgets import QApplication
from mainWindow import MainWindow

import os
import shutil
import sys

def main():
    miscFiles = ["config.ini", "columns_info.json", "image_labels.csv", "icon.jpg"]
    copyMiscFiles(miscFiles)
    app = QApplication(sys.argv)
    cont = MainWindow()
    # removeMiscFiles(miscFiles) UNCOMMENT THIS EVENTUALLY
    app.exec_()

def copyMiscFiles(miscFiles):
    if hasattr(sys, "_MEIPASS"): # Single file
        pass
    else: # Not single file
        cxrRootFolder = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        miscFolderAbsPath = os.path.join(cxrRootFolder, "miscellaneous")
        for miscFile in miscFiles:
            if not os.path.exists(miscFile):
                shutil.copyfile(os.path.join(miscFolderAbsPath, miscFile), miscFile)

def removeMiscFiles(miscFiles):
    for miscFile in miscFiles:
        os.remove(miscFile)

if __name__ == "__main__":
    main()