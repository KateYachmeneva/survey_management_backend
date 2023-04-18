import copy
import math
import os
from math import sin, cos
from random import random, randint

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

file_dir = os.getcwd() + "\\Files"


def getGorizontalAxes(Inc1, Inc2, Az1, Az2, deltaMD):
    """
    Получаем шаг по X,Y,Z для горизонтальной проекции
    """
    dInc = math.radians(Inc2 - Inc1)
    dAzim = math.radians(Az2-Az1)
    I1 = math.radians(Inc1)
    I2 = math.radians(Inc2)
    A1 = math.radians(Az1)
    A2 = math.radians(Az2)

    beta = math.acos(cos(dInc) - sin(I1) * sin(I2) * (1 - cos(dAzim)))
    # beta = (1 if beta == 0 else beta)
    RF = (2 / beta) * math.tan(beta / 2) if beta != 0 else 1

    deltaX = (deltaMD / 2) * (sin(I1) * cos(A1) + sin(I2) * cos(A2)) * RF
    deltaY = (deltaMD / 2) * (sin(I1) * sin(A1) + sin(I2) * sin(A2)) * RF
    deltaZ = (deltaMD / 2) * (cos(I1) + cos(I2)) * RF

    # print("beta ", beta, " RF ", RF, ' deltaTVD ', deltaZ, 'deltaNS ', deltaX, ' deltaEW ', deltaY)
    return deltaX, deltaY, deltaZ


def getVerticalAxes(NS2: int, EW2: int, VSaz: int) -> int:
    """
        Получаем шаг по Vsect2, ClsDisp2 для вертикальной проекции
        """

    ClsDisp2 = math.sqrt(NS2 ** 2 + EW2 ** 2)

    if ClsDisp2 == 0:
        ClsAz2 = 0
    elif NS2 < 0:
        ClsAz2 = math.atan(EW2 / NS2) * 180 / math.pi + 180
    else:
        ClsAz2 = math.atan(EW2 / NS2) * 180 / math.pi

    # print(f'NS: {NS2} | EW: {EW2} | ClsAz2: {ClsAz2}')
    delta_for_cos = (ClsAz2 - VSaz) * math.pi / 180
    Vsect2 = cos(delta_for_cos) * ClsDisp2
    # print(f"VSaz: {VSaz} |  ClsDisp: {ClsDisp2} | ClsAz2: {ClsAz2} | Vsect: {Vsect2} ")
    return Vsect2, ClsDisp2


def get_graph_data(I: list, A: list, Depth: list, RKB: int, VSaz: int = 1) -> list:
    """
    I - угол
    А - азимут
    Depth - глубина
    RKB - высота ствола ротора (параметры скважины)
    VSaz - азимут вертикальной секции (параметры скважины)
    Здесь получаем данные для постройки горизонтальной и вертикальной проекции
    EW_list - запад/восток,
    NS_list - север/юг,
    Vsect_list, TVDSS_list, TVD_list

    """
    TVD = 0
    TVDSS = RKB
    Vsect = 0
    NS = 0
    EW = 0

    ClsDisp = 0
    NS_list: list() = [0, ]
    EW_list: list() = [0, ]
    Vsect_list: list() = [0, ]
    TVDSS_list: list() = [RKB, ]
    TVD_list: list() = [0, ]

    all_measurement = list(zip(Depth, I, A))
    print('-----------------------')
    for i, meas in enumerate(all_measurement):
        if meas[0] == all_measurement[-1][0]:
            # print(f'break - {all_measurement[-1][0]}')
            break
        # print(meas[0])
        deltaNS, deltaEW, deltaTVD = getGorizontalAxes(Inc1=meas[1],
                                                       Inc2=all_measurement[i + 1][1],
                                                       Az1=meas[2],
                                                       Az2=all_measurement[i + 1][2],
                                                       deltaMD=(all_measurement[i + 1][0] - meas[0]))
        # print(f'Vsect {Vsect} | TVD {TVD} | TVDSS {TVDSS}')


        # print(f"delta: {deltaNS, deltaEW, deltaTVD}")

        NS += deltaNS
        EW += deltaEW
        TVD += deltaTVD
        TVDSS -= deltaTVD  # TVD

        Vsect, ClsDisp = getVerticalAxes(NS2=NS,
                                         EW2=EW,
                                         VSaz=VSaz)
        # print('Depth ', all_measurement[i + 1][0], ' NS ', NS, ' EW ', EW)
        NS_list.append(NS)
        EW_list.append(EW)
        Vsect_list.append(Vsect)
        TVD_list.append(TVD)
        TVDSS_list.append(TVDSS)
    return EW_list, NS_list, Vsect_list, TVDSS_list, TVD_list


# def add_plot(x, y, name):
#     # Подаем в функцию x y для каждой из линий с соответсвующими надписями
#     getHorizontalPlot(NS_list, EW_list, 'План')
#     plt.close()
#     getVerticalPlot(TVDSS_list, Vsect_list, 'План')
#     plt.close()

data_name = {'igirgi_file': 'Статические замеры ИГИРГИ',
             'nnb_dynamic': 'Динамические замеры ННБ',
             'nnb_static': 'Статические замеры ННБ',
             'raw_file': 'Сырые динамические замеры',
             'plan_traj_file': 'Плановая траектория',
             'igirgi_dynamic': 'Динамические замеры ИГИРГИ',
             }


def get_graphics(all_data: dict, well: object) -> dict:
    """
    Строит график, сохраняет его в /Report_out/1.png
    На выходе словарь с данными для записи в эксель
    Ключи в словаре:
            -nnb_delta_y
            -nnb_delta_x
            -nnb_TVD
            -igirgi_TVDSS
            -igirgi_delta_y
            -igirgi_delta_x
            -igirgi_TVD
    """
    RKB = (84 if well.RKB is None else well.RKB)
    VSaz = (1 if well.VSaz is None else well.VSaz)

    data_dict = dict()  # словарь с данными, которые необходимо записать в эксель

    fig = plt.figure(figsize=(15, 15))

    ax1 = fig.add_subplot(2, 2, 1)
    ax2 = fig.add_subplot(2, 2, 2)

    fig.subplots_adjust(wspace=0.5, hspace=0.5)

    data = all_data['Плановая траектория']
    x1, y1, x2, y2, z = get_graph_data(I=data['Угол'],
                                       A=data['Азимут'],
                                       Depth=data['Глубина'],
                                       RKB=RKB,
                                       VSaz=VSaz)

    ext_dict = {'min_x': min(x1),  # для границ графика
                'max_x': max(x1),
                'min_y': min(y1),
                'max_y': max(y1)}

    ax1.plot(x1, y1, 'g', label='Плановая траектория')
    ax2.plot(x2, y2, 'g', label='Плановая траектория')

    data = all_data['Статические замеры ННБ']
    x1, y1, x2, y2, z = get_graph_data(I=data['Угол'],
                                       A=data['Азимут'],
                                       Depth=data['Глубина'],
                                       RKB=RKB,
                                       VSaz=VSaz)
    # ext_list.extend([min(x1), max(x1), min(y1), max(y1)])
    ax1.plot(x1, y1, 'b', label='Подрядчик по ННБ')
    ax2.plot(x2, y2, 'b', label='Подрядчик по ННБ')

    data_dict['nnb_TVD'] = copy.deepcopy(z)
    data_dict['nnb_delta_y'] = copy.deepcopy(y1)
    data_dict['nnb_delta_x'] = copy.deepcopy(x1)

    data = all_data['Статические замеры ИГИРГИ']
    x1, y1, x2, y2, z = get_graph_data(I=data['Угол'],
                                       A=data['Азимут'],
                                       Depth=data['Глубина'],
                                       RKB=RKB,
                                       VSaz=VSaz)

    ax1.plot(x1, y1, color='orange', label='IGIRGI')
    ax2.plot(x2, y2, color='orange', label='IGIRGI')

    # for item in zip(x1, y1, x2, y2, z, data['Глубина']):
    #     print(f"NS: {item[0]} | EW: {item[1]} | Vsect: {item[2]} | TVDSS: {item[3]} | TVD: {item[4]} | DEPTH: {item[5]}")

    data_dict['igirgi_TVD'] = copy.deepcopy(z)
    data_dict['igirgi_TVDSS'] = copy.deepcopy(y2)
    data_dict['igirgi_delta_y'] = copy.deepcopy(y1)
    data_dict['igirgi_delta_x'] = copy.deepcopy(x1)

    if 'Динамические замеры ННБ' in all_data.keys():
        data = all_data['Динамические замеры ННБ']
        x1, y1, x2, y2, z = get_graph_data(I=data['Угол'],
                                           A=data['Азимут'],
                                           Depth=data['Глубина'],
                                           RKB=RKB,
                                           VSaz=VSaz)
        ax2.plot(x2, y2, 'b--', label='ННБ_Din')

    if 'Динамические замеры ИГИРГИ' in all_data.keys():
        data = all_data['Динамические замеры ИГИРГИ']
        x1, y1, x2, y2, z = get_graph_data(I=data['Угол'],
                                           A=data['Азимут'],
                                           Depth=data['Глубина'],
                                           RKB=RKB,
                                           VSaz=VSaz)
        ax2.plot(x2, y2, '--', color='orange', label='IGIRGI_Din')

    # собественные границы графиков
    step = 6  # на грфике 6 шагов
    delta_x = (ext_dict['max_x'] - ext_dict['min_x'])
    delta_y = (ext_dict['max_y'] - ext_dict['min_y'])

    # # Создаем экземпляр класса, который будет отвечать за расположение рисок
    # # Риски будут следовать с шагом delta
    # locator = matplotlib.ticker.MultipleLocator(delta_y if delta_x > delta_y else delta_x)
    #
    # # Установим локатор для главных рисок
    # ax1.xaxis.set_major_locator(locator)
    # ax1.yaxis.set_major_locator(locator)

    if delta_x > delta_y:
        ext_dict['max_y'] += (delta_x - delta_y)/2
        ext_dict['min_y'] -= (delta_x - delta_y)/2
        additional_delta = delta_x / (step * 2)
    else:
        ext_dict['max_x'] += (delta_y - delta_x)/2
        ext_dict['min_x'] -= (delta_y - delta_x)/2
        additional_delta = delta_y / (step * 2)

    # создаем квадратную сетке
    ax1.set_xlim(ext_dict['min_x'] - additional_delta, ext_dict['max_x'] + additional_delta)
    ax1.set_ylim(ext_dict['min_y'] - additional_delta, ext_dict['max_y'] + additional_delta)

    ax1.set_xlabel('Запад/Восток')
    ax1.set_ylabel('Юг/Север')
    ax1.set_title('Горизонтальная проекция')
    ax1.legend(title='Вертикальная проекция', loc=(0, -0.4), mode='expand', ncols=1)
    ax1.grid()
    ax2.set_xlabel('Вертикальная секция')
    ax2.set_ylabel('Абсолютная отметка')
    ax2.set_title('Вертикальная проекция')
    ax2.legend(title='Вертикальная проекция', bbox_to_anchor=(0.85, -0.15))
    ax2.grid()

    plt.savefig(file_dir + f'/Report_out/{well}.png')

    return data_dict
