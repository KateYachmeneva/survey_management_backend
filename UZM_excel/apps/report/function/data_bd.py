from ..models import *
import collections


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
