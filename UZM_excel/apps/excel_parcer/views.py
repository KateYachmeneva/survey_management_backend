from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage

from .forms import AddDeviceForm
from .function.functions import *

from django.http import JsonResponse, HttpResponse
import re
from Field.views_api import get_tree
from Field.models import Well, Run, Wellbore, Run, get_all_run, Section, get_all_well
from .models import Data, TelesystemIndex, Device


def index(request):
    """
    Оси вывод по рейсам данных
    """
    context = {"title": 'Оси',
               "run": get_all_run(),
               "wellbores_id": list(),  # повторяет run только с индексами скважин
               'selected_run': 'None',
               'error_depth': list(),  # глубины замеров при вставке которых нашли ошибку
               "telesystem": Device.objects.all(),
               }
    # Для сохранения в SessionStorage на клиенте id выбранной скважине по рейсу
    for run in context['run']:
        context['wellbores_id'].append(run.section.wellbore.id)

    if request.method == 'POST':
        # получение данных для отображения
        try:
            current_run = Run.objects.get(id=request.POST['run'])
        except Exception as e:
            print(e)
            return render(request, 'excel_parcer/data.html', {'context': context, })
        context['well'] = current_run.section.wellbore.well_name
        context['data'] = Data.objects.filter(run=request.POST['run'], in_statistics=1).order_by('depth')
        context['selected_run'] = current_run

        if 'data-axes' in request.POST:  # Модальная форма с ОСЯМИ
            axes_data = request.POST['data-axes'].replace(',', '.'). \
                replace(' ', '').replace('\r', '').replace('\n', '\t').split('\t')
            counter = 0
            manually_bz = list()
            manually_by = list()
            manually_bx = list()
            manually_gz = list()
            manually_gy = list()
            manually_gx = list()
            manually_depth = list()
            for data in axes_data:
                if data == '':
                    continue
                if counter == 0:
                    manually_depth.append(data)
                elif counter == 1:
                    manually_gx.append(data)
                elif counter == 2:
                    manually_gy.append(data)
                elif counter == 3:
                    manually_gz.append(data)
                elif counter == 4:
                    manually_bx.append(data)
                elif counter == 5:
                    manually_by.append(data)
                else:
                    manually_bz.append(data)
                counter = (0 if counter == 6 else counter + 1)
            # result - считанные данные
            result = zip(manually_depth, manually_gx, manually_gy, manually_gz, manually_bx, manually_by, manually_bz)
            if request.POST.get('device') != '-----' and request.POST.get('device') != '':
                telesystem_ind = TelesystemIndex.objects.get(run_id=current_run)
                telesystem_ind.device = Device.objects.get(device_title=request.POST.get('device'))
                telesystem_ind.save()
                result2 = new_measurements(list(result), request.POST.get('device'))  # перобразованные данные
                write_to_bd(result2, current_run)
            else:
                write_to_bd(result, current_run)
        if 'depth' in request.POST:  # Модальная форма с  Скорректированными значениями
            depth_data = request.POST['depth'].replace(',', '.').replace(' ', '').replace('\r', ''). \
                replace('\n', '\t').split('\t')
            Btotal_data = request.POST['Btotal_corr'].replace(',', '.').replace(' ', '').replace('\r', ''). \
                replace('\n', '\t').split('\t')
            DIP_data = request.POST['DIP_corr'].replace(',', '.').replace(' ', '').replace('\r', ''). \
                replace('\n', '\t').split('\t')
            for meas in zip(depth_data, Btotal_data, DIP_data):
                if meas[0] != '' and meas[1] != '' and meas[2] != '':
                    try:
                        obj = Data.objects.get(run=current_run, depth=float(meas[0]))
                        obj.Btotal_corr = (float(meas[1]) if float(meas[1]) > 100 else float(meas[1]) * 1000)
                        obj.DIP_corr = float(meas[2])
                        obj.save()
                    except:
                        context['error_depth'].append(float(meas[0]))
    return render(request, 'excel_parcer/data.html', {'context': context, })


def edit_index(request):
    """Редактировать таблицу с осями и скорректирвоанными значениями"""
    context = {"title": 'Оси',
               'selected_run': 'None',
               }

    if request.method == 'GET':
        if request.GET.get('run_id'):
            current_run = Run.objects.get(id=request.GET.get('run_id'))
            context['well'] = current_run.section.wellbore.well_name
            context['data'] = Data.objects.filter(run=current_run, in_statistics=1).order_by('depth')
            context['selected_run'] = current_run

    # FIXME
    if request.method == 'POST':
        for items in request.POST.lists():
            key = str(items[0]).split(' ')
            try:
                obj = Data.objects.get(id=key[0])
            except:
                continue
                print('Замер уже удалён')

            if items[1][0] == '':
                if key[1] == 'btotal':
                    obj.Btotal_corr = None
                    obj.save()
                elif key[1] == 'dip':
                    obj.DIP_corr = None
                    obj.save()
                else:
                    obj.delete()
            else:
                if key[1] == 'depth':
                    obj.depth = items[1][0]
                elif key[1] == 'gx':
                    obj.CX = items[1][0]
                elif key[1] == 'gy':
                    obj.CY = items[1][0]
                elif key[1] == 'gz':
                    obj.CZ = items[1][0]
                elif key[1] == 'bx':
                    obj.BX = items[1][0]
                elif key[1] == 'by':
                    obj.BY = items[1][0]
                elif key[1] == 'bz':
                    obj.BZ = items[1][0]
                elif key[1] == 'btotal':
                    obj.Btotal_corr = items[1][0]
                elif key[1] == 'dip':
                    obj.DIP_corr = items[1][0]
                obj.save()
        return redirect('axes')
    return render(request, 'excel_parcer/edit_data.html', {'context': context, })


def file(request):
    """добавление данных \add"""
    context = {"telesystem": Device.objects.all(),
               "run": get_all_run(),
               "title": 'Загрузка осей',
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


def add_Device(request):
    """добавление телесистемы"""
    context = {"telesystem": Device.objects.all(),
               "title": 'Телесистема',
               "form": AddDeviceForm(request.POST),
               }

    if request.method == 'POST':
        if context['form'].is_valid():
            context['form'].save()
    return render(request, 'excel_parcer/device.html', {'context': context, })


def graph(request):
    """Страница с графиком первичного контроля"""
    context = {'title': 'Контроль качества', "tree": get_tree(), 'depthGoxy': list(),
               'depthGz': list(), 'depthGtotal': list(), 'depthGref': list(), 'depthGmax': list(), 'depthGmin': list(),
               'depthBoxy': list(), 'depthBz': list(), 'depthBtotal': list(), 'depthBref': list(), 'depthBmax': list(),
               'depthBmin': list(), 'depthBcorr': list(), 'depthDipraw': list(), 'depthDipref': list(),
               'depthDipmax': list(), 'depthDipmin': list(), 'depthDipcorr': list(), 'depthHSTF': list(),
               'selected': 'None'}

    if request.method == 'POST' and request.POST['wellbore'] != '':
        wellbore = Wellbore.objects.get(id=request.POST['wellbore'])
        runs = Run.objects.filter(section__wellbore=wellbore)
        context['selected'] = wellbore
        for run in runs:
            surveys = Data.objects.filter(run=run)
            for survey in surveys:
                # График Goxy-Gz
                context['depthGoxy'].append({'x': survey.depth, 'y': survey.get_goxy()})
                context['depthGz'].append({'x': survey.depth, 'y': survey.CZ})
                # График Gtotal
                context['depthGtotal'].append({'x': survey.depth, 'y': survey.Gtotal()})
                context['depthGref'].append({'x': survey.depth, 'y': wellbore.well_name.gtotal_graph()})
                context['depthGmax'].append({'x': survey.depth, 'y': wellbore.well_name.max_gtotal()})
                context['depthGmin'].append({'x': survey.depth, 'y': wellbore.well_name.min_gtotal()})
                # График Boxy-Bz
                context['depthBoxy'].append({'x': survey.depth, 'y': survey.get_boxy()})
                context['depthBz'].append({'x': survey.depth, 'y': survey.BZ})
                # График Btotal
                context['depthBtotal'].append({'x': survey.depth, 'y': survey.Btotal()})
                context['depthBref'].append({'x': survey.depth, 'y': wellbore.well_name.btotal_graph()})
                context['depthBmax'].append({'x': survey.depth, 'y': wellbore.well_name.max_btotal()})
                context['depthBmin'].append({'x': survey.depth, 'y': wellbore.well_name.min_btotal()})
                context['depthBcorr'].append({'x': survey.depth, 'y': (survey.Btotal_corr if
                                                                       survey.Btotal_corr is not None else 'Null')})
                # График HSTF
                context['depthHSTF'].append({'x': survey.depth, 'y': survey.get_hstf()})
                # График Dip
                context['depthDipraw'].append({'x': survey.depth, 'y': survey.Dip()})
                context['depthDipref'].append({'x': survey.depth, 'y': wellbore.well_name.dip_graph()})
                context['depthDipmax'].append({'x': survey.depth, 'y': wellbore.well_name.max_dip()})
                context['depthDipmin'].append({'x': survey.depth, 'y': wellbore.well_name.min_dip()})
                context['depthDipcorr'].append({'x': survey.depth, 'y': (survey.DIP_corr if
                                                                         survey.DIP_corr is not None else 'Null')})

    try:
        context['firstDepth'] = context['depthHSTF'][0]['x']
        context['lastDepth'] = context['depthHSTF'][-1]['x']
    except IndexError:
        context['firstDepth'] = context['lastDepth'] = 0

    return render(request, 'excel_parcer/graph.html', {'context': context, })


def del_Meas(request):
    """Удаление замеров POST методом"""
    for key, value in request.POST.dict().items():
        Data.objects.get(id=key).delete()
    return JsonResponse({'status': 'ok'})


def del_Device(request):
    """Удаление телистемы по id"""
    dev = Device.objects.get(id=request.POST['device_id']).delete()
    return JsonResponse({'status': 'ok'})


def get_coef_device(request):
    """api для fetch запроса
    Получаем коэффициенты
    """
    try:
        device = Device.objects.get(device_title=request.POST.get('device_title'))
    except:
        return JsonResponse({'status': str(request.POST.get('device_title')) + '- такой телесистемы нет', })

    return JsonResponse({
        'GX': device.CX,
        'GY': device.CY,
        'GZ': device.CZ,
        'BX': device.BX,
        'BY': device.BY,
        'BZ': device.BZ,
    })


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
