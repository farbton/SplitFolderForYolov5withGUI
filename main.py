# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 12:35:03 2024

@author: Admin
"""


import sys; print("sys.version: ", sys.version)
from PyQt5 import QtWidgets
import mainwindow


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = mainwindow.Window(app)
    mainWindow.show()
    mainWindow.start()
    app.exec_()
