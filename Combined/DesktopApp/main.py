import sys
from PyQt5.QtWidgets import QApplication
from mainWindow import MainWindow

def main():
    app = QApplication(sys.argv)
    cont = MainWindow()
    app.exec_()

if __name__ == "__main__":
    main()