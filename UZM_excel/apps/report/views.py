import os
import time

from PIL import Image
from django.http import JsonResponse, FileResponse, HttpResponse
from django.shortcuts import render, redirect
from drf_yasg.openapi import Response

# Create your views here.
from .function.api_func import get_index
from .function.graffic import get_graphics
from .function.model_service import get_data, clone_wellbore_traj, NNBToIgirgi
from .function.work_with_Excel import write_data_in_Excel
from .function.work_with_data import rewrite_ReportIndex, work_with_file, plan_delete, work_with_nnb
from Field.models import get_all_run, Run, Wellbore
from .models import *
from .serializer import ProjectionParamSerializer


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
        obj = ReportIndex.objects.get_or_create(run=Run.objects.get(id=request.POST['run']))
        obj[0].nnb_static_depth = request.POST['nnb_depth']
        obj[0].nnb_static_corner = request.POST['nnb_corner']
        obj[0].nnb_static_azimut = request.POST['nnb_azimut']
        obj[0].nnb_static_list_name = request.POST['nnb_list_name']
        obj[0].nnb_static_read = request.POST['nnb_str']
        obj[0].nnb_static_exclude_proj = (True if request.POST.get('nnb_exclude_proj') is not None else False)
        obj[0].save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'Warning_Text': 'нужно обращение к post методу'})


# report/api/file_name
def report(request):
    """Делаем отчёт по имеющимся данным и отправляем его имя"""
    # по рейсу ищем все остальные рейсы скважины
    run = Run.objects.get(id=request.POST['run_id'])
    runs = Run.objects.filter(section__wellbore=run.section.wellbore)
    all_data = get_data(runs)
    file_name, waste = write_data_in_Excel(all_data, f'Единая_форма_отчета.xlsx', run)  # имя файла и отходы
    return JsonResponse({'file_name': file_name, 'waste': waste})


# report/api/get_file
def get_report_file(request):
    """Получаем файл по имени """
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
    meas = IgirgiStatic.objects.get(id=request.POST['id'])
    meas.comment = request.POST['comment']
    meas.save()
    return JsonResponse({'status': 'ok'})


# report/api/meas_del
def traj_del(request):
    """ По fetch запросу с клиента удаляем замеры траектории по id"""
    for key, value in request.POST.dict().items():
        if 'igirgi' in key:
            igirgi_meas = IgirgiStatic.objects.get(id=value)
            igirgi_meas.delete()
            try:  # удалить план вместе с игирги
                interp_plan = InterpPlan.objects.get(run=igirgi_meas.run, depth=igirgi_meas.depth)
                interp_plan.delete()
            except InterpPlan.DoesNotExist:
                pass
        elif 'nnb' in key:
            if request.POST.get('type') == 'plan':
                InterpPlan.objects.get(id=value).delete()
            else:
                StaticNNBData.objects.get(id=value).delete()
        else:
            continue
    return JsonResponse({'status': 'ok'})


# report/api/graph
def get_graph(request):
    """ Вывод картинки с вертикальной/горизонтальной проекциями """
    wellbor_id = request.POST.get('wellbore_id')
    if wellbor_id is None or wellbor_id == 'null':
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
    try:
        index = ReportIndex.objects.get(run=r_id)
        NoneCorrectItems = {None, ''}
        Items = {index.nnb_static_depth, index.nnb_static_corner, index.nnb_static_azimut, index.nnb_static_list_name, }
        if len(NoneCorrectItems.intersection(Items)) != 0:
            raise ReportIndex.DoesNotExist
    except ReportIndex.DoesNotExist:
        return JsonResponse({'error': 'Ошибка чтения! Пожалуйста, проверьте настройки импорта для '
                                      'выбранного рейса!'})

    if f_type is None:
        return JsonResponse({'status': 'Файл передан без типа. Укажите в поле type один из параметров:',
                             'type': '(nnb, plan, igirgi)'})
    if r_id is None:
        return JsonResponse({'status': 'Не был передан id рейса. Укажите номер id в поле "run_id".'})

    run = Run.objects.get(id=r_id)
    if f_type == 'nnb':
        work_with_nnb(request, run)

    return JsonResponse({'status': 'ok'})


def proj_param(request, wellbore_id):
    """ Параметры для графика проекций горизонтальной/вертикальной"""

    if request.method == 'GET':
        try:
            params = ProjectionParam.objects.get(wellbore=wellbore_id)
            return JsonResponse(ProjectionParamSerializer(params).data)
        except ProjectionParam.DoesNotExist:
            return JsonResponse({'warning': 'Не удалось найти параметры по данному id ствола.'})

    if request.method == 'POST':
        if wellbore_id is None:
            return JsonResponse({'warning': 'Не указан id ствола! Укажите id в параметре wellbore_id.'})
        else:
            try:
                w = Wellbore.objects.get(id=wellbore_id)
            except Exception as e:
                return JsonResponse({'warning': 'Ствол с указанным id не существует!'})

        obj = ProjectionParam.objects.get_or_create(wellbore=w)
        # print(request.POST.dict())
        # проверка на наличие коэффициентов
        hor = True
        ver = True
        hor_x_min = request.POST.get('hor_x_min')
        hor_x_max = request.POST.get('hor_x_max')
        hor_x_del = request.POST.get('hor_x_del')
        hor_y_min = request.POST.get('hor_y_min')
        hor_y_max = request.POST.get('hor_y_max')
        hor_y_del = request.POST.get('hor_y_del')

        if None or '' in (hor_x_min, hor_x_max, hor_x_del, hor_y_min, hor_y_max, hor_y_del):
            hor = False
        else:
            obj[0].hor_x_min = hor_x_min
            obj[0].hor_x_max = hor_x_max
            obj[0].hor_x_del = hor_x_del
            obj[0].hor_y_min = hor_y_min
            obj[0].hor_y_max = hor_y_max
            obj[0].hor_y_del = hor_y_del

        ver_x_min = request.POST.get('ver_x_min')
        ver_x_max = request.POST.get('ver_x_max')
        ver_x_del = request.POST.get('ver_x_del')
        ver_y_min = request.POST.get('ver_y_min')
        ver_y_max = request.POST.get('ver_y_max')
        ver_y_del = request.POST.get('ver_y_del')

        if None or '' in (ver_x_min, ver_x_max, ver_x_del, ver_y_min, ver_y_max, ver_y_del):
            ver = False
        else:
            obj[0].ver_x_min = ver_x_min
            obj[0].ver_x_max = ver_x_max
            obj[0].ver_x_del = ver_x_del
            obj[0].ver_y_min = ver_y_min
            obj[0].ver_y_max = ver_y_max
            obj[0].ver_y_del = ver_y_del

        if not ver and not hor:
            return JsonResponse({'warning': 'Не заполнены обязательные параметры!'})

        # print(obj)
        obj[0].save()
        return JsonResponse({'status': 'ок'})

#
# def comment_copy(request):
#     num = NNBToIgirgi()
#     return JsonResponse({"Не было найдено комментариев:": f"{num}"})
