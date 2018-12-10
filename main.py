import MainWindow
from PyQt4 import QtCore, QtGui

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow2 = QtGui.QMainWindow()
    ui = MainWindow.Ui_MainWindow()
    ui.setupUi(MainWindow2)
    MainWindow2.show()
    MainWindow.cambiarLCD(4)
    sys.exit(app.exec_())
