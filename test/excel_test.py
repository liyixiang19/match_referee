import time

from PyQt5.QtWidgets import QMessageBox
from xlsxwriter import Workbook
import xlwt
from excel_generate import switch_excel


class SaveExcel(object):
    def __init__(self):
        pass

    def get_excel(self, recoder_dict, column_name):
        now = time.strftime("%Y%m%d-%H%M%S", time.localtime())
        wb = Workbook("result_" + now + ".xlsx")
        ws = wb.add_worksheet("New Sheet")  # or leave it blank, default name is "Sheet 1"

        ws.set_column("A:X", 13)  # 设置列宽度
        ws.set_row(0, 30)  # 设置行高度

        cell_fmt = {'bold': False, 'font_name': '微软雅黑', 'font_size': 10, 'align': 'center', 'valign': 'vcenter',
                    'border': 0, 'text_wrap': True}
        header_fmt = {'bold': True, 'font_name': '微软雅黑', 'font_size': 10, 'align': 'center', 'valign': 'vcenter',
                      'border': 0, 'bg_color': '#808080', 'text_wrap': True}
        cell_format = wb.add_format(cell_fmt)
        header_format = wb.add_format(header_fmt)

        first_row = 0
        for header in column_name:
            col = column_name.index(header)  # we are keeping order.
            ws.write(first_row, col, header, header_format)  # we have written first row which is the header of worksheet also.

        row = 1
        for recoder in recoder_dict:
            print(recoder)
            for _key, _value in recoder_dict[recoder].items():
                print(_key, _value)
                col = column_name.index(_key)
                ws.write(row, col, _value, cell_format)
            row += 1  # enter the next row
        print("-------------------------")
        wb.close()


if __name__ == '__main__':
    li = switch_excel.SaveExcel()
    map1 = {"1": {'name': '123', 'nation': '中国（China）', 'number': '5', 'referee_name': '231', '1_status': 'success_in',
                  '1_time_use': '3', '1_image_path': 'D:\\Projects\\picture\\4.jpg', '1_repair': 'no',
                  '2_repair': 'yes',
                  '2_status': 'touch_out', '2_time_use': '2', '2_image_path': 'D:\\Projects\\picture\\9.jpg',
                  '3_status':
                      'mother_ball_in', '3_time_use': '4', '3_image_path': 'D:\\Projects\\picture\\6.jpg', '3_repair':
                      'no', '4_status': 'out_area', '4_time_use': '5', '4_image_path': 'D:\\Projects\\picture\\0.jpg',
                  '4_repair': 'no', '5_status': 'touch_ball', '5_time_use': '4', '5_image_path':
                      'D:\\Projects\\picture\\0.jpg', '5_repair': 'no'}}

    column_list = ["name", "nation", "number", "referee_name", "1_status", "1_time_use", "1_image_path", "1_repair",
                   "2_status", "2_time_use", "2_image_path", "2_repair",
                   "3_status", "3_time_use", "3_image_path", "3_repair",
                   "4_status", "4_time_use", "4_image_path", "4_repair",
                   "5_status", "5_time_use", "5_image_path", "5_repair"]

    li.get_excel(map1, column_list)
    print("信息已保存！")

