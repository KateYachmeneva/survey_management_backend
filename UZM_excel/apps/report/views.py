import os
import time

from django.http import JsonResponse, FileResponse, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from .function.api_func import get_index
from .function.graffic import get_graphics
from .function.model_service import get_data, clone_wellbore_traj
from .function.work_with_Excel import write_data_in_Excel
from .function.work_with_data import rewrite_ReportIndex, work_with_file, plan_delete, work_with_nnb
from Field.models import get_all_run, Run, Wellbore
from .models import *


# def index(request):
#     """Главная страница для генератора отчетов [Больше не используется]"""
#
#     context = {"title": 'Отчет',
#                "run": get_all_run(), }
#
#     if request.method == 'POST':
#         index_id = rewrite_ReportIndex(request.POST.dict())  # перезапись индексов, получаем id текущего рейса
#         igirgi_data = request.POST['igirgi_data'].replace(',', '.').replace(' ', '') \
#             .replace('\r', '').replace('\n', '\t').split('\t')
#
#         if len(igirgi_data) < 3:  # фиксируем отсутсвие ручного ввода
#             igirgi_data = None
#
#         return work_with_file(request=request,
#                               run_id=request.POST.dict()['run'],
#                               index_id=index_id,
#                               igirgi_data=igirgi_data)
#
#     return render(request, 'report/index.html', {'context': context, })


# report/api/run_index
def run_index(request):
    """Функция для fetch запроса [получаем индексы для считывания файлов]"""
    if request.method == 'POST':
        return get_index(request)
    return JsonResponse({'Warning_Text': 'нужно обращение к post методу'})


# report/api/update_index
def update_index(request):
    """Функция для fetch запроса ля обнавления индексов под считывание файлов"""
    if request.method == 'POST':
        # print(request.POST.dict())
        obj = ReportIndex.objects.get(run=request.POST['run'])
        obj.nnb_static_depth = request.POST['nnb_depth']
        obj.nnb_static_corner = request.POST['nnb_corner']
        obj.nnb_static_azimut = request.POST['nnb_azimut']
        obj.nnb_static_list_name = request.POST['nnb_list_name']
        obj.nnb_static_read = request.POST['nnb_str']
        obj.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'Warning_Text': 'нужно обращение к post методу'})


# report/api/file_name
def report(request):
    """Делаем отчёт по имеющимся данным и отправляем его имя"""
    # по рейсу ищем все остальные рейсы скважины
    run = Run.objects.get(id=request.POST['run_id'])
    runs = Run.objects.filter(section__wellbore=run.section.wellbore)
    all_data = get_data(runs)
    file_name, waste = write_data_in_Excel(all_data, f'Единая_форма_отчета0.xlsx', 0, run)  # имя файла и отходы
    return JsonResponse({'file_name': file_name, 'waste': waste})


# report/api/get_file
def get_report_file(request):
    """Пролучаем файл по имени """
    # print('Беру отчёт с сервера!')
    file_name = request.POST['name']
    file_dir = os.getcwd() + "\\files"
    return FileResponse(open(file_dir + "\\Report_out\\" + file_name, 'rb'))


# report/api/wellbore_copy
def wellbore_copy(request):
    """ По fetch запросу с клиента клонируются замеры ствола
    (в request должны лежать id нового и старого стволов, сама модель Wellbore создается в модуле Field заранее)"""
    clone_wellbore_traj(Wellbore.objects.get(id=request.POST['old_wellbore']),
                        Wellbore.objects.get(id=request.POST['new_wellbore']))
    time.sleep(3)  # Данные не успевают добавиться в базу до отображения на странице
    return JsonResponse({'status': 'ok'})


# report/api/plan_del
def plan_del(request):
    """ По fetch запросу с клиента удаляем замеры плана по указанному id"""
    # удаляем старый план
    plan_delete(Run.objects.get(id=request.POST['run_id']))
    return JsonResponse({'status': 'ok'})


# report/api/traj_comm
def put_comment(request):
    """Обновить/создать комментарий у замера ННБ"""
    meas = StaticNNBData.objects.get(id=request.POST['id'])
    meas.comment = request.POST['comment']
    meas.save()
    return JsonResponse({'status': 'ok'})


# report/api/meas_del
def traj_del(request):
    """ По fetch запросу с клиента удаляем замеры траектории по id"""
    for key, value in request.POST.dict().items():
        if 'igirgi' in key:
            IgirgiStatic.objects.get(id=value).delete()
        elif 'nnb' in key:
            StaticNNBData.objects.get(id=value).delete()
        else:
            continue
    return JsonResponse({'status': 'ok'})


# report/api/graph
def get_graph(request):
    """ Вывод картинки с вертикальной/горизонтальной проекциями """
    wellbor_id = request.POST.get('wellbore_id')
    if wellbor_id is None:
        return JsonResponse({'status': 'Укажите id скважины в параметре wellbore_id.'})
    wellbore = Wellbore.objects.get(id=wellbor_id)
    try:
        img = open(os.getcwd() + f"\\Files\\Report_out\\{wellbore}.png", 'rb')
    except FileNotFoundError:
        runs = Run.objects.filter(section__wellbore=wellbore)
        all_data = get_data(runs)
        get_graphics(all_data, wellbore)
        img = open(os.getcwd() + f"\\Files\\Report_out\\{wellbore}.png", 'rb')

    response = FileResponse(img)
    return response


# report/api/upload_file
def uploadFile(request):
    """ Сюда будут приходить файлы для считывания траектории с fetch запросов """
    f_type = request.POST.get('type')  # пытаемся найти тип файла (траектория ннб или плановая)
    r_id = request.POST.get('run_id')
    if f_type is None:
        return JsonResponse({'status': 'Файл передан без типа. Укажите в поле type один из параметров:',
                             'type': '(nnb, plan, igirgi)'})
    if r_id is None:
        return JsonResponse({'status': 'Не был передан id рейса. Укажите номер id в поле "run_id".'})

    run = Run.objects.get(id=r_id)
    if f_type == 'nnb':
        work_with_nnb(request, run)

    return JsonResponse({'status': 'ok'})
