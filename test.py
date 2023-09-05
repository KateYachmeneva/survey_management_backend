# import re
#
# text = ('Талипов Руслан Дамирович <TalipovRD@skn.rosneft.ru>; Шарипов Булат Рифгатович <SharipovBR@skn.rosneft.ru>;'
#         ' Григорьев Алексей Сергеевич <AS_Grigorev6@skn.rosneft.ru>; SM_SEVKOM <SM_SEVKOM@igirgi.su>;'
#         ' #СевКомНефтегаз, ООО: ОГСБС <GSB@skn.rosneft.ru>; ')
#
# text2 = 'Группа ГИС <Group.GIS@igirgi.su>; Довиденков Антон Леонидович <a_dovidenkov@igirgi.su>; Зарипова Лиана Фанисовна <Ly_Zaripova@igirgi.su>; Михайлова Татьяна Алексеевна <T_Mihaylova@igirgi.su>; Бойчук Диана Юрьевна <d_boychuk@igirgi.su>; Журавлева Карина Константиновна <k_zhuravleva@igirgi.su>'
#
# print(''.join(str(s)+"; " for s in re.findall('<(\S*)>', text2)))

with open("C:\\Users\\a_dovidenkov\\Downloads\\Данные для тестов\\TMN_1_277-2_BS_INCL_RT_MD_2770.txt") as my_file:
    line = my_file.readline()
    while line:
        print(repr())
        line = my_file.readline()

