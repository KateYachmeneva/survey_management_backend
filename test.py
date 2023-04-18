# import openpyxl
# from openpyxl import Workbook, load_workbook
# import lasio
#
# path = 'C:\\Users\\a_dovidenkov\\Downloads\\SKN_22005_Run500_Gx_Gy_Gz_Bx_By_Bz.xlsx'
#
# excel_file = openpyxl.load_workbook(path, data_only=True)
# excel_sheet = excel_file.worksheets[0]
#
# data = []
# colum_id = 2
# for row_id in range(int(3), excel_sheet.max_row + 1000):
#     cell = excel_sheet.cell(row_id, colum_id)
#     if cell.value is not None:
#         data.append(cell.value)
# print(data)

import smtplib as smtp

login = 'ant.dovidenkov9458@gmail.com'
password = 'GodWarrior87'

server = smtp.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(login, password)

subject = 'какая-нибудь тема письма. может быть пустой'
text = 'основной текст письма. тоже можно оставить пустым'

server.sendmail(login, 'DovidenkovAL@igirgi.rosneft.ru', f'Subject:{subject}\n{text}')

