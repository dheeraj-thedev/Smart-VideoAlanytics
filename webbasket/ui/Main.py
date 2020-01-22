from PyQt5.QtWidgets import QVBoxLayout, QSlider

__author__ = 'Dheeraj Singh'

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Main.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!

from webbasket.ui.ImageViewer import VideoWindow
from PyQt5 import QtCore, QtGui, QtWidgets, Qt


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(715, 525)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.mdiArea = QtWidgets.QMdiArea(self.centralwidget)
        self.mdiArea.setGeometry(QtCore.QRect(-1, -1, 701, 491))
        self.mdiArea.setObjectName("mdiArea")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 715, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuConfig = QtWidgets.QMenu(self.menubar)
        self.menuConfig.setObjectName("menuConfig")
        self.menuSystem = QtWidgets.QMenu(self.menubar)
        self.menuSystem.setObjectName("menuSystem")
        self.menuConfig_2 = QtWidgets.QMenu(self.menuSystem)
        self.menuConfig_2.setObjectName("menuConfig_2")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionLogin = QtWidgets.QAction(MainWindow)
        self.actionLogin.setObjectName("actionLogin")
        self.actionCameraConfig = QtWidgets.QAction(MainWindow)
        self.actionCameraConfig.setObjectName("actionCameraConfig")
        self.actionCamera_Config = QtWidgets.QAction(MainWindow)
        self.actionCamera_Config.setObjectName("actionCamera_Config")
        self.actionSystem_Value = QtWidgets.QAction(MainWindow)
        self.actionSystem_Value.setObjectName("actionSystem_Value")
        self.menuFile.addAction(self.actionLogin)
        self.menuConfig_2.addAction(self.actionCamera_Config)
        self.menuConfig_2.addAction(self.actionSystem_Value)
        self.menuSystem.addAction(self.menuConfig_2.menuAction())
        self.menuSystem.addAction(self.actionCameraConfig)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuConfig.menuAction())
        self.menubar.addAction(self.menuSystem.menuAction())
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.video = VideoWindow(parent=self.mdiArea)




    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuConfig.setTitle(_translate("MainWindow", "View"))
        self.menuSystem.setTitle(_translate("MainWindow", "System"))
        self.menuConfig_2.setTitle(_translate("MainWindow", "Config"))
        self.actionLogin.setText(_translate("MainWindow", "Open Video"))
        self.actionCameraConfig.setText(_translate("MainWindow", "pen"))
        self.actionCamera_Config.setText(_translate("MainWindow", "Camera Config"))
        self.actionSystem_Value.setText(_translate("MainWindow", "System Value"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    #app = QApplication(sys.argv)
    player = VideoWindow(parent=MainWindow)
    player.resize(640, 480)
    #player.show()
    #sys.exit(app.exec_())
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
