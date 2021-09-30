from ui5_4 import Ui_MainWindow
import sys
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QFileDialog, QMainWindow
from PyQt5.QtWidgets import QMessageBox
class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
       super().__init__()
       self.setupUi(self)
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myWin =  MyMainWindow()
    myWin.setWindowTitle('运动康复系统')
    myWin.show()
    sys.exit(app.exec_())