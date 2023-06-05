from math import sqrt

from ..models import *
from django.db.models import Max
from .graffic import *


def get_data(run: object) -> dict:
    """
    Функция для перезаписи даты в работу, опираясь на данные из бд.
    (Если у нас  в БД лежит план траектории то необязательно он должен быть в форме со страницы)
    """
    data = {'Статические замеры ИГИРГИ': IgirgiStatic.objects.filter(run=run),
            'Динамические замеры ННБ': DynamicNNBData.objects.filter(run=run),
            'Статические замеры ННБ': StaticNNBData.objects.filter(run=run),
            'Плановая траектория': Plan.objects.filter(run=run),
            'Динамические замеры ИГИРГИ': IgirgiDynamic.objects.filter(run=run),
            }

    del_key = list()
    # преобразуем queryset в словарь с листами (3 отдельных массива - Глубина,Угол,Азимут)
    for key, queryset in data.items():
        if len(queryset) != 0:
            meas_lists = {'Глубина': list(),
                          'Угол': list(),
                          'Азимут': list(),
                          }

            for meas in queryset:
                meas_lists['Глубина'].append(meas.depth)
                meas_lists['Угол'].append(meas.corner)
                meas_lists['Азимут'].append(meas.azimut)
            data[key] = meas_lists
        else:
            del_key.append(key)

    for key in del_key:
        data.pop(key)

    return data


def last_depth(Well: object):
    """ Получить последнюю точку замера cкважины"""
    return IgirgiStatic.objects.filter(run__section__wellbore__well_name=Well).aggregate(Max('depth'))['depth__max']


def waste(Well: object):
    """ Формируем отходы по последней точке"""
    nnb = StaticNNBData.objects.filter(run__section__wellbore__well_name=Well).order_by('depth')
    igirgi = IgirgiStatic.objects.filter(run__section__wellbore__well_name=Well).order_by('depth')

    RKB = (84 if Well.RKB is None else Well.RKB)
    VSaz = (1 if Well.VSaz is None else Well.VSaz)
    data = {'Угол': list(), 'Азимут': list(), 'Глубина': list()}

    for meas in nnb:
        data['Угол'].append(meas.corner)
        data['Азимут'].append(meas.azimut)
        data['Глубина'].append(meas.depth)

    nnb_delta_x, nnb_delta_y, x2, y2, nnb_delta_TVD = get_graph_data(I=data['Угол'],
                                                                     A=data['Азимут'],
                                                                     Depth=data['Глубина'],
                                                                     RKB=RKB,
                                                                     VSaz=VSaz)

    for meas in igirgi:
        data['Угол'].append(meas.corner)
        data['Азимут'].append(meas.azimut)
        data['Глубина'].append(meas.depth)

    igirgi_delta_x, igirgi_delta_y, x2, y2, igirgi_delta_TVD = get_graph_data(I=data['Угол'],
                                                                              A=data['Азимут'],
                                                                              Depth=data['Глубина'],
                                                                              RKB=RKB,
                                                                              VSaz=VSaz)

    # пошли отходы
    Ex = (Well.EX if Well.EX is not None else 0)
    Ny = (Well.NY if Well.NY is not None else 0)
    for meas in zip(igirgi_delta_x, igirgi_delta_y, igirgi_delta_TVD, nnb_delta_x, nnb_delta_y, nnb_delta_TVD):
        X_nnb = Ex + meas[4]
        Y_nnb = Ny + meas[3]

        X_igirgi = Ex + meas[1]
        Y_igigri = Ny + meas[0]

        horiz = round(sqrt((X_nnb - X_igirgi) ** 2 + (Y_nnb - Y_igigri) ** 2), 2)  # отход по горизонтали
        vert = round(meas[3] - meas[5], 2)  # отход по вертикали
        departure = round(
            sqrt((X_nnb - X_igirgi) ** 2 + (Y_nnb - Y_igigri) ** 2 + (meas[3] - meas[5]) ** 2),
            2)  # отход общий
    return horiz, vert, departure
