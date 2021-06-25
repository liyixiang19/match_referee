from xlsxwriter import Workbook


class SaveExcel(object):
    def __init__(self):
        pass

    def get_excel(self, recoder_dict, column_name):
        wb = Workbook("result.xlsx")
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
            ws.write(first_row, col, header,
                     header_format)  # we have written first row which is the header of worksheet also.

        row = 1
        for recoder in recoder_dict:
            print(recoder)
            for _key, _value in recoder_dict[recoder].items():
                print(_key, _value)
                col = column_name.index(_key)
                ws.write(row, col, _value, cell_format)
            row += 1  # enter the next row
        print("-----------生成excel结束--------------")
        wb.close()
