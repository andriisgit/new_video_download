# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitter = QtWidgets.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.links_view = QtWidgets.QListView(self.splitter)
        self.links_view.setObjectName("links_view")
        self.videos_view = QtWidgets.QListView(self.splitter)
        self.videos_view.setObjectName("videos_view")
        self.horizontalLayout.addWidget(self.splitter)
        self.videos_view.raise_()
        self.splitter.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menu_add_playlist = QtWidgets.QAction(MainWindow)
        self.menu_add_playlist.setEnabled(False)
        self.menu_add_playlist.setVisible(False)
        self.menu_add_playlist.setObjectName("menu_add_playlist")
        self.menu_add_video = QtWidgets.QAction(MainWindow)
        self.menu_add_video.setObjectName("menu_add_video")
        self.menu_quit = QtWidgets.QAction(MainWindow)
        self.menu_quit.setObjectName("menu_quit")
        self.menu.addAction(self.menu_add_video)
        self.menu.addAction(self.menu_add_playlist)
        self.menu.addSeparator()
        self.menu.addAction(self.menu_quit)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menu.setTitle(_translate("MainWindow", "??????????????????????"))
        self.menu_add_playlist.setText(_translate("MainWindow", "???????????? ???? ?????????????????????? PLAYLIST ..."))
        self.menu_add_video.setText(_translate("MainWindow", "???????????? ?????????????????? ???? VIDEOS ..."))
        self.menu_quit.setText(_translate("MainWindow", "??????????"))
