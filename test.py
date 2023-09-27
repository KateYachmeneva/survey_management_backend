# import re
#
# text = ('Талипов Руслан Дамирович <TalipovRD@skn.rosneft.ru>; Шарипов Булат Рифгатович <SharipovBR@skn.rosneft.ru>;'
#         ' Григорьев Алексей Сергеевич <AS_Grigorev6@skn.rosneft.ru>; SM_SEVKOM <SM_SEVKOM@igirgi.su>;'
#         ' #СевКомНефтегаз, ООО: ОГСБС <GSB@skn.rosneft.ru>; ')
#
# text2 = 'Группа ГИС <Group.GIS@igirgi.su>; Довиденков Антон Леонидович <a_dovidenkov@igirgi.su>; Зарипова Лиана Фанисовна <Ly_Zaripova@igirgi.su>; Михайлова Татьяна Алексеевна <T_Mihaylova@igirgi.su>; Бойчук Диана Юрьевна <d_boychuk@igirgi.su>; Журавлева Карина Константиновна <k_zhuravleva@igirgi.su>'
#
# print(''.join(str(s)+"; " for s in re.findall('<(\S*)>', text2)))

import sqlite3


def progress(status, remaining, total):
    print(f'Копирование {total-remaining} из {total} страниц...')


try:
    sqlite_con = sqlite3.connect('F:\\Рабочий стол\\GIT\\UZM_excel\\db.sqlite3')
    backup_con = sqlite3.connect('F:\\Рабочий стол\\GIT\\UZM_excel\\Бэкап\\backup.db')
    with backup_con:
        sqlite_con.backup(backup_con, pages=1, progress=progress)
    print("Резервное копирование выполнено успешно")
except sqlite3.Error as error:
    print("Ошибка при резервном копировании: ", error)
finally:
    if (backup_con):
        backup_con.close()
        sqlite_con.close()

