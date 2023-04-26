from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

from UZM_excel.conf import server_ip
from .function.functions import *

from django.http import JsonResponse, HttpResponse
import re

from Field.models import get_all_run, Run

from .models import Data, TelesystemIndex, Device


def index(request):
    """
    Оси вывод по рейсам данных
    """
    context = {"title": 'Оси',
               "run": get_all_run(),
               'selected_run': 'Выберите рейс'
               }

    if request.method == 'POST':
        current_run = Run.objects.get(id=request.POST['run'])
        context['well'] = current_run.section.wellbore.well_name
        context['data'] = Data.objects.filter(run=request.POST['run']).order_by('depth')
        context['selected_run'] = current_run
    return render(request, 'excel_parcer/parcer.html', {'context': context, })


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

    return render(request, 'excel_parcer/data.html', {'context': context, })


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


def AxeGraphImage(request, run_id):
    with open(f'C:/Users/superuser/UZM_excel/files/Report_out/{run_id}.png', "rb") as f:
        return HttpResponse(f.read(), content_type="image/jpeg")


def graph(request):
    """Страница с графиком первичного контроля"""
    context = {"title": 'График',
               "run": get_all_run(),
               'data': [],
               }
    return render(request, 'excel_parcer/graph.html', {'context': context, })
