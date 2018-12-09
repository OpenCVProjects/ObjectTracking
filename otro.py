import sys
import MainWindow
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = MainWindow.MainWindow()
    counterPeople()
    mainWin.show()
    sys.exit( app.exec_() )
