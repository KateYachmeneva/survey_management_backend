from math import sqrt
from typing import Union, Iterable, NoReturn

from ..models import *
from django.db.models import Max
from .graffic import *
from Field.models import Run


def get_data(runs: Union[object, Iterable[object]]) -> dict:
    """
    Функция для перезаписи даты в работу, опираясь на данные из бд.
    (Если у нас  в БД лежит план траектории то необязательно он должен быть в форме со страницы)
    """

    if len(runs) == 0:  # передали не массив рейсов а один рейс
        run = runs
        data = {'Статические замеры ИГИРГИ': IgirgiStatic.objects.filter(run=run),
                'Динамические замеры ННБ': DynamicNNBData.objects.filter(run=run),
                'Статические замеры ННБ': StaticNNBData.objects.filter(run=run),
                'Плановая траектория': Plan.objects.filter(run=run),
                'Динамические замеры ИГИРГИ': IgirgiDynamic.objects.filter(run=run),
                }
    else:
        data = {'Статические замеры ИГИРГИ': IgirgiStatic.objects.filter(run__in=runs),
                'Динамические замеры ННБ': DynamicNNBData.objects.filter(run__in=runs),
                'Статические замеры ННБ': StaticNNBData.objects.filter(run__in=runs),
                'Плановая траектория': Plan.objects.filter(run__in=runs),
                'Динамические замеры ИГИРГИ': IgirgiDynamic.objects.filter(run__in=runs),
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
            del_key.append(key)  # удаляем те ключи у которых нет данных (например если нет динамических замеров)

    for key in del_key:
        data.pop(key)

    # добавим точку привязки, начальный 0
    if data['Статические замеры ИГИРГИ']['Глубина'][0] != 0:
        data['Статические замеры ИГИРГИ']['Глубина'] = [0, *data['Статические замеры ИГИРГИ']['Глубина']]
        data['Статические замеры ИГИРГИ']['Угол'] = [0, *data['Статические замеры ИГИРГИ']['Угол']]
        data['Статические замеры ИГИРГИ']['Азимут'] = [0, *data['Статические замеры ИГИРГИ']['Азимут']]

    if data['Плановая траектория']['Глубина'][0] != 0:
        data['Плановая траектория']['Глубина'] = [0, *data['Плановая траектория']['Глубина']]
        data['Плановая траектория']['Угол'] = [0, *data['Плановая траектория']['Угол']]
        data['Плановая траектория']['Азимут'] = [0, *data['Плановая траектория']['Азимут']]

    if data['Статические замеры ННБ']['Глубина'][0] != 0:
        data['Статические замеры ННБ']['Глубина'] = [0, *data['Статические замеры ННБ']['Глубина']]
        data['Статические замеры ННБ']['Угол'] = [0, *data['Статические замеры ННБ']['Угол']]
        data['Статические замеры ННБ']['Азимут'] = [0, *data['Статические замеры ННБ']['Азимут']]

    return data


def last_depth(Wellbore: object):
    """ Получить последнюю точку замера cкважины"""
    return IgirgiStatic.objects.filter(run__section__wellbore=Wellbore).aggregate(Max('depth'))['depth__max']


def waste(Wellbore: object, full: int = 0):
    """ Формируем отходы по последней точке
    Если full то выдает весь массив отходов"""
    nnb = StaticNNBData.objects.filter(run__section__wellbore=Wellbore).order_by('depth')
    igirgi = IgirgiStatic.objects.filter(run__section__wellbore=Wellbore).order_by('depth')

    RKB = (84 if Wellbore.well_name.RKB is None else Wellbore.well_name.RKB)
    VSaz = (1 if Wellbore.well_name.VSaz is None else Wellbore.well_name.VSaz)
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
    data = {'Угол': list(), 'Азимут': list(), 'Глубина': list()}
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
    Ex = (Wellbore.well_name.EX if Wellbore.well_name.EX is not None else 0)
    Ny = (Wellbore.well_name.NY if Wellbore.well_name.NY is not None else 0)

    if full == 1:
        horiz = list()
        vert = list()
        departure = list()

    for meas in zip(igirgi_delta_x, igirgi_delta_y, igirgi_delta_TVD, nnb_delta_x, nnb_delta_y, nnb_delta_TVD):
        X_nnb = Ex + meas[4]
        Y_nnb = Ny + meas[3]

        X_igirgi = Ex + meas[1]
        Y_igigri = Ny + meas[0]

        if full == 1:
            horiz.append(round(sqrt((X_nnb - X_igirgi) ** 2 + (Y_nnb - Y_igigri) ** 2), 2))
            vert.append(round(meas[5] - meas[2], 2))
            departure.append(
                round(sqrt((X_nnb - X_igirgi) ** 2 + (Y_nnb - Y_igigri) ** 2 + (meas[2] - meas[5]) ** 2), 2))
            continue
        horiz = round(sqrt((X_nnb - X_igirgi) ** 2 + (Y_nnb - Y_igigri) ** 2), 2)  # отход по горизонтали
        vert = round(meas[5] - meas[2], 2)  # отход по вертикали
        departure = round(
            sqrt((X_nnb - X_igirgi) ** 2 + (Y_nnb - Y_igigri) ** 2 + (meas[2] - meas[5]) ** 2),
            2)  # отход общий
    return horiz, vert, departure


def clone_wellbore_data(old_wellbore: object, new_wellbore: object) -> str:
    """Клонирование всех замеров старого ствола в новый ствол"""
    for old_section in old_wellbore.sections.all():
        for old_run in old_section.runs.all():
            new_run = Run.objects.get(run_number=old_run.run_number, section__wellbore=new_wellbore)

            for meas in IgirgiStatic.objects.filter(run=old_run):
                IgirgiStatic.objects.create(run=new_run, depth=meas.depth, corner=meas.corner, azimut=meas.azimut)

            for meas in StaticNNBData.objects.filter(run=old_run):
                StaticNNBData.objects.create(run=new_run, depth=meas.depth, corner=meas.corner, azimut=meas.azimut)
    return 'Ok'
