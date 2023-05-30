from ..models import *
from django.db.models import Max


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
    return IgirgiStatic.objects.filter(run__section__wellbore__well_name=Well).aggregate(Max('depth'))


def waste(Well: object):
    depth = last_depth(Well)
    StaticNNBData.objects.filter(run__section__wellbore__well_name=Well, depth=depth)
    IgirgiStatic.objects.filter(run__section__wellbore__well_name=Well, depth=depth)
    # пошли отходы
    Ex = (Well.EX if Well.EX is not None else 0)
    Ny = (Well.NY if Well.NY is not None else 0)
#     X_nnb = Ex + meas[10]
#     Y_nnb = Ny + meas[9]
#
#     X_igirgi = Ex + meas[7]
#     Y_igigri = Ny + meas[6]
#
#     excel_sheet.cell(row=row, column=10).value = round(  # отход по горизонтали
#         sqrt((X_nnb - X_igirgi) ** 2 + (Y_nnb - Y_igigri) ** 2), 2)
#     excel_sheet.cell(row=row, column=11).value = round(meas[11] - meas[8], 2)  # отход по вертикали
#     excel_sheet.cell(row=row, column=12).value = round(  # отход общий
#         sqrt((X_nnb - X_igirgi) ** 2 + (Y_nnb - Y_igigri) ** 2 +
#              (meas[11] - meas[8]) ** 2), 2)
#
# def ar():
#     pass
