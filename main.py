import os
import random
import sys
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QMainWindow, QFileDialog
from ui import match_control, image_projection
from info_check import before_check
from excel_save import switch_excel


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.clock)
        self.main_ui = match_control.Ui_match_control()
        self.main_ui.setupUi(self)
        # 初始值
        self.random_image_path = ""
        self.repair_times = 2
        self.remain_hit_times = 5
        self.time_use = 0
        self.time_default = 60
        self.counter = 60
        self.score = 0
        self.recoder = {}
        self.status = ""
        # 定义赛前检查标志位
        self.before_check = before_check.BeforeCheck(self.main_ui)
        self.main_ui.spinBox_ballsuccessin1.valueChanged.connect(lambda : self.hit_result("success_in"))
        self.main_ui.spinBox_touchout1.valueChanged.connect(lambda : self.hit_result("touch_out"))
        self.main_ui.spinBox_outarea1.valueChanged.connect(lambda : self.hit_result("out_area"))
        self.main_ui.spinBox_motherballin1.valueChanged.connect(lambda : self.hit_result("mother_ball_in"))
        self.main_ui.spinBox_touchball1.valueChanged.connect(lambda : self.hit_result("touch_ball"))

    def hit_result(self, status):
        print("击球结果 =====>  " + status)
        self.status = status

    @pyqtSlot()
    def on_toolButton_enter_match_clicked(self):
        print("裁判员点击进入比赛，系统检查赛前准备工作完成情况...")

        if 1 == self.before_check.info_input_check():
            print("队伍信息输入完整！")
        else:
            QMessageBox.information(self, '信息提示对话框', "参赛队伍信息输入不完全，请裁判员重新检查！")
            print("参赛队伍信息输入不完全，请裁判员重新检查！")
            return

        if 1 == self.before_check.match_before_check():
            print("检查完成，请开始比赛！")
            # 存储比赛队伍信息
            info = {"name": self.main_ui.lineEdit_name.text(), "nation": self.main_ui.comboBox_country.currentText(),
                    "number": self.main_ui.lineEdit_partnernumber.text(), "referee_name":
                        self.main_ui.lineEdit_referee_name.text()}
            self.recoder[self.main_ui.comboBox_id.currentText()] = info
            print("参赛队伍信息 ==> " + str(self.recoder))
        else:
            QMessageBox.information(self, '信息提示对话框', "赛前检查未完成，请裁判员重新检查！")
            print("赛前检查未完成，请裁判员重新检查！")

    @pyqtSlot()
    def on_Button_random_image1_clicked(self):
        random_num = random.randint(0, 9)
        self.random_image_path = os.path.abspath('.') + "\\picture\\" + str(random_num) + ".jpg"
        print("随机生成方案图片路径： " + self.random_image_path)
        self.main_ui.lineEdit_image_path1.setText(self.random_image_path)

    @pyqtSlot()
    def on_Button_open_image1_clicked(self):
        if "" == self.random_image_path:
            QMessageBox.information(self, '信息提示对话框', "请先生成图片随机路径！")
            print("请先生成图片随机路径！")
            return
        jpg = QtGui.QPixmap(self.random_image_path)
        self.main_ui.label_show_image1.setScaledContents(True)
        self.main_ui.label_show_image1.setPixmap(jpg)

    @pyqtSlot()
    def on_Button_projection1_clicked(self):
        if "" == self.random_image_path:
            QMessageBox.information(self, '信息提示对话框', "请先生成图片随机路径！")
            print("请先生成图片随机路径！")
            return
        projection_win = ProjectionWindow(self.random_image_path)
        projection_win.paintEngine()
        projection_win.showFullScreen()
        projection_win.exec_()

    @pyqtSlot()
    def on_Button_match_start1_clicked(self):
        if self.remain_hit_times > 0:
            print("============>第【" + str(5-self.remain_hit_times + 1) + "】次击球开始, 开始计时<===========")
            self.timer.start(1000)
        else:
            QMessageBox.information(self, '信息提示对话框', "击球次数已用完！")
            print("击球次数已用完！")

    def clock(self):
        if self.counter >= 0:
            self.main_ui.lcdNumber1.display(self.counter)
            self.counter -= 1
        else:
            self.timer.stop()

    @pyqtSlot()
    def on_Button_match_stop1_clicked(self):
        # 每次点击结束代表一次击球次数结束
        print(">>>>单次击球任务结束<<<<")
        self.timer.stop()
        # 用时
        self.time_use = self.time_default - self.counter
        self.counter = self.time_default

    @pyqtSlot()
    def on_Button_match_once_stop1_clicked(self):
        # 剩余次数
        self.remain_hit_times -= 1
        self.main_ui.lineEdit_remain_times1.setText(str(self.remain_hit_times))
        # 记录本次击球的状态
        self.recoder[self.main_ui.comboBox_id.currentText()][str(5 - self.remain_hit_times) + "_status"] = self.status
        self.recoder[self.main_ui.comboBox_id.currentText()][str(5 - self.remain_hit_times) + "_time_use"] = str(self.time_use)
        self.recoder[self.main_ui.comboBox_id.currentText()][str(5 - self.remain_hit_times) + "_image_path"] = self.random_image_path
        if str(5 - self.remain_hit_times) + "_repair" not in self.recoder[self.main_ui.comboBox_id.currentText()]:
            self.recoder[self.main_ui.comboBox_id.currentText()][str(5 - self.remain_hit_times) + "_repair"] = "no"
        print(str(self.recoder))
        repair_result = self.recoder[self.main_ui.comboBox_id.currentText()][str(5 - self.remain_hit_times) + "_repair"]
        print("第【%d】次击球信息 ==> 队伍序号:【%s】| 击球结果:【%s】| 用时:【%d】| 图片路径:【%s】| 是否维修:【%s】" % (
              5 - self.remain_hit_times, str(self.main_ui.comboBox_id.currentText()), self.status, self.time_use,
              self.random_image_path, repair_result))

    @pyqtSlot()
    def on_Button_device_repair1_clicked(self):
        print("队伍申请维修，比赛暂停，计时器重置")
        self.main_ui.lcdNumber1.display(self.time_default)
        if self.repair_times > 0:
            self.repair_times -= 1
            self.recoder[self.main_ui.comboBox_id.currentText()][str(5 - self.remain_hit_times + 1) + "_repair"] = "yes"
            self.main_ui.lineEdit_remain_repair_times1.setText(str(self.repair_times))
            self.timer.stop()
            self.counter = self.time_default
        else:
            QMessageBox.information(self, '信息提示对话框', "维修次数已用完！")
            print("维修次数已用完！")

    @pyqtSlot()
    def on_Button_compute_points1_clicked(self):
        print(">>>>>开始计算分数<<<<<<<")
        # todo 计算公式

        self.score = 100
        print("参赛队伍：【%s】 ==> 最后得分：【%d】" % (self.main_ui.lineEdit_name.text(), self.score))
        self.recoder[self.main_ui.comboBox_id.currentText()]["score"] = str(self.score)
        self.main_ui.lineEdit_score1.setText(str(self.score))

    @pyqtSlot()
    def on_Button_save1_clicked(self):
        print("开始导出本队比赛结果,请稍等...")
        print(self.recoder)
        save_excel = switch_excel.SaveExcel()
        column_list = ["name", "nation", "number", "referee_name", "1_status", "1_time_use", "1_image_path", "1_repair",
                       "2_status", "2_time_use", "2_image_path", "2_repair",
                       "3_status", "3_time_use", "3_image_path", "3_repair",
                       "4_status", "4_time_use", "4_image_path", "4_repair",
                       "5_status", "5_time_use", "5_image_path", "5_repair"]
        save_excel.get_excel(self.recoder, column_list)


class ProjectionWindow(QDialog):
    def __init__(self, image_path):
        QMainWindow.__init__(self)
        self.image_path = image_path
        self.projection_ui = image_projection.Ui_Form()
        self.projection_ui.setupUi(self)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawRect(self.rect())
        img = QtGui.QPixmap(self.image_path)
        painter.drawPixmap(self.rect(), img)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())
