import sys
import time
import socket
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QMainWindow
from ui import match_control
from info_check import before_check


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.main_ui = match_control.Ui_match_control()
        self.main_ui.setupUi(self)

        # 定义赛前检查标志位
        self.before_check = before_check.BeforeCheck(self.main_ui)


    @pyqtSlot()
    def on_toolButton_entermatch_clicked(self):
        print("裁判员点击进入比赛，系统检查赛前准备工作完成情况...")

        if 1 == self.before_check.info_input_check():



        if 1 == self.before_check.match_before_check():
            print("检查完成，请开始比赛！")
        else:
            QMessageBox.information(self, '信息提示对话框', "赛前检查未完成，请裁判员重新检查！")
            print("赛前检查未完成，请裁判员重新检查！")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
