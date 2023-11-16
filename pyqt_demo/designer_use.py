# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from test_designer import Ui_Form


# GUI class
class MyMainForm(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)

        self.pushButton.clicked.connect(self.display)
    
    def display(self):
        username = self.lineEdit.text()
        password = self.lineEdit_2.text()

        self.textBrowser.setText('Log in successfully!\n Username is %s\n Password is %s' % (username, password))


# main
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainForm()
    myWin.show()
    sys.exit(app.exec_())
