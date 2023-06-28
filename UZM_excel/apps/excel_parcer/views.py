from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

from UZM_excel.conf import server_ip
from .function.functions import *

from django.http import JsonResponse, HttpResponse
import re

from Field.models import Run, get_all_run
from .models import Data, TelesystemIndex, Device


def index(request):
    """
    Оси вывод по рейсам данных
    """
    context = {"title": 'Оси',
               "run": get_all_run(),
               "wells_id": list(),  # повторяет run только с индексами скважин
               'selected_run': 'None'
               }
    for run in context['run']:
        context['wells_id'].append(run.section.wellbore.well_name.id)

    if request.method == 'POST':
        current_run = Run.objects.get(id=request.POST['run'])
        context['well'] = current_run.section.wellbore.well_name
        context['data'] = Data.objects.filter(run=request.POST['run'], in_statistics=1).order_by('depth')
        context['selected_run'] = current_run
        if 'data' in request.POST:  # ловим данные с модальной формы
            axes_data = request.POST['data'].replace(',', '.').replace(' ', '').replace('\r', '').replace('\n', '\t') \
                .split('\t')
            counter = 0
            for data in axes_data:
                if data == '':
                    continue
                if counter == 0:
                    obj = Data.objects.get_or_create(run=current_run, depth=data)[0]
                elif counter == 1:
                    obj.CX = data
                elif counter == 2:
                    obj.CY = data
                elif counter == 3:
                    obj.CZ = data
                elif counter == 4:
                    obj.BX = data
                elif counter == 5:
                    obj.BY = data
                else:
                    obj.BZ = data
                    obj.in_statistics = 1
                    obj.save()
                counter = (0 if counter == 6 else counter + 1)
        if 'depth' in request.POST:  # ловим данные с модальной формы
            depth_data = request.POST['depth'].replace(',', '.').replace(' ', '').replace('\r', '').replace('\n', '\t') \
                .split('\t')
            Btotal_data = request.POST['Btotal_corr'].replace(',', '.').replace(' ', '').replace('\r', '').replace('\n',
                                                                                                                   '\t') \
                .split('\t')
            DIP_data = request.POST['DIP_corr'].replace(',', '.').replace(' ', '').replace('\r', '').replace('\n', '\t') \
                .split('\t')
            for meas in zip(depth_data, Btotal_data, DIP_data):
                try:
                    obj = Data.objects.get(run=current_run, depth=meas[0])
                    obj.Btotal_corr = (meas[1] if meas[1] < 100 else meas[1] * 1000)
                    obj.DIP_corr = meas[2]
                    obj.save()
                except:
                    pass

    return render(request, 'excel_parcer/data.html', {'context': context, })


def file(request):
    """добавление данных \add"""
    context = {"telesystem": Device.objects.all(),
               "run": get_all_run(),
               "title": 'Загрузка осей',
               'server_ip': server_ip,  # для прокидывания fetch запросов js
               }

    if request.method == 'POST':
        if 'file' in request.FILES:
            doc = request.FILES['file']
            fs = FileSystemStorage()
            file_name = fs.save(doc.name, doc)  # сохраняем файл для дальнейшего считывания
            current_run = Run.objects.get(id=request.POST.get('run'))
            update_values = {'GX': request.POST.get('manually_gx'),
                             'GY': request.POST.get('manually_gy'),
                             'GZ': request.POST.get('manually_gz'),
                             'BX': request.POST.get('manually_bx'),
                             'BY': request.POST.get('manually_by'),
                             'BZ': request.POST.get('manually_bz'),
                             'depth': request.POST.get('manually_depth'),
                             'units': request.POST.get('manually_measurement'),
                             'string_index': request.POST.get('manually_import'),
                             'device': Device.objects.get(device_title=request.POST.get('device'))}
            TelesystemIndex.objects.update_or_create(run=current_run, defaults=update_values)
            result = parcing_manually("./media/" + file_name, request.POST.get('manually_depth'),
                                      request.POST.get('manually_gx'), request.POST.get('manually_gy'),
                                      request.POST.get('manually_gz'), request.POST.get('manually_bx'),
                                      request.POST.get('manually_by'), request.POST.get('manually_bz'),
                                      request.POST.get('manually_import'))
            result2 = new_measurements(result, request.POST.get('device'))
            context['result2'] = result2
            context['result'] = result
            write_to_bd(result2, current_run)

    return render(request, 'excel_parcer/add_data.html', {'context': context, })


def get_run_index(request):
    """api для fetch запроса
    Получаем индексы для выбранного рейса
    """
    if request.method == 'POST':
        telesystem_tuple = TelesystemIndex.objects.get_or_create(run=Run.objects.get(id=request.POST.get('run_title')))
        telesystem_index = telesystem_tuple[0]
        try:
            return JsonResponse({
                'GX': telesystem_index.GX,
                'GY': telesystem_index.GY,
                'GZ': telesystem_index.GZ,
                'BX': telesystem_index.BX,
                'BY': telesystem_index.BY,
                'BZ': telesystem_index.BZ,
                'unit': telesystem_index.units,
                'string': telesystem_index.string_index,
                'depth': telesystem_index.depth,
                'device': telesystem_index.device.device_title, })
        except Exception as e:
            return JsonResponse({
                'GX': [],
                'GY': [],
                'GZ': [],
                'BX': [],
                'BY': [],
                'BZ': [],
                'unit': [],
                'string': [],
                'depth': [],
                'device': [],
            })