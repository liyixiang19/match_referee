from ui import match_control


class BeforeCheck(object):

    def __init__(self, ui):
        self.ui = ui
        pass

    def info_input_check(self):
        # 队伍信息录入
        if 0 == self.ui.comboBox_id.currentText():
            print("请选择队伍序号")
            return 0
        if "" == self.ui.lineEdit_name.text():
            print("请输入参赛队伍名称")
            return 0
        if "无" == self.ui.comboBox_country.currentText():
            print("请选择参赛队伍国籍！")
            return 0
        return 1

    def match_before_check(self):
        # 赛前检查流程
        if self.ui.checkBox_partnerinfo.isChecked():
            print("参赛人员身份确认！")
        else:
            print("请裁判员确认参赛人员身份")
            return 0

        if self.ui.checkBox_ballclub.isChecked():
            print("击球球杆确认！")
        else:
            print("请裁判员确认击球球杆")
            return 0

        if self.ui.checkBox_workarea.isChecked():
            print("装置工作范围确认！")
        else:
            print("请裁判员确认装置工作范围")
            return 0

        if self.ui.checkBox_sizeweight.isChecked():
            print("装置尺寸质量确认！")
        else:
            print("请裁判员确认装置尺寸质量")
            return 0

        if self.ui.checkBox_camerainfo.isChecked():
            print("视觉系统确认！")
        else:
            print("请裁判员确认视觉系统")
            return 0

        if self.ui.checkBox_AGVinfo.isChecked():
            print("AGV工作状态确认！")
        else:
            print("请裁判员确认AGV工作状态")
            return 0

        if self.ui.checkBox_teamready.isChecked():
            print("队伍准备就绪！")
        else:
            print("请裁判员确认队伍准备情况")
            return 0

        if "" != self.ui.lineEdit_referee_name.text():
            print("裁判员姓名确认！")
        else:
            print("请裁判员输入姓名")
            return 0

        print("裁判员完成赛前检查")
        return 1
