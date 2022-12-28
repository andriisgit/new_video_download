from PyQt5 import QtCore, QtGui, QtWidgets
from window.date_form import Ui_Dialog


class DateDialog(QtWidgets.QDialog):
    def __init__(self):
        super(DateDialog, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
