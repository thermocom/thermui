#!/usr/bin/python3

import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import *
import thermui


class Therm_Main(QWidget):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.ui = thermui.Ui_Form()
        self.ui.setupUi(self)

def main(args):
    app = QApplication(args)

    topwindow = Therm_Main()
    topwindow.show()
    
    sys.exit(app.exec_())


if __name__=="__main__":
    main(sys.argv)
