from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from pytest import console_main
from Field.models import Well, Run, get_all_well
from excel_parcer.models import Data
from report.models import StaticNNBData, IgirgiStatic, Plan
from report.function.work_with_data import work_with_plan
from Field.views_api import get_tree
from .function.context_editer import *
from .function.mail import *
from report.function.work_with_Excel import write_data_in_Excel
from UZM_excel.conf import server_ip


def index(request):
    """Главная страница"""
    context = {"title": 'Работа с данными',
               }

    if request.method == 'POST':
        pass

    return render(request, 'data_handler/index.html', {'context': context, })


def traj(request):
    """Страница с траекторией ННБ и ИГиРГИ"""
    context = {"title": 'Траектория',
               "active": 'traj',
               "tree": get_tree(),
               "server_ip": server_ip,
               }
    # print(context['tree'])
    if request.method == "GET":
        if request.GET.get('run_id') is not None:  # если в get запросе не run_id выводим пустую страницу
            run_id = request.GET.get('run_id')
            run = Run.objects.get(id=run_id)
            context['selected_obj'] = str(run)  # для отображения текущей модели на странице
            context['selected_id'] = run_id  # для перенаправления по id на редактирование

            selected_for_tree(context, run)  # для раскрытия списка

            context["igirgi_data"] = IgirgiStatic.objects.filter(run=run_id)
            context["nnb_data"] = StaticNNBData.objects.filter(run=run_id)
            runs = Run.objects.filter(section__wellbore__well_name=run.section.wellbore.well_name)
            context["plan_ex"] = (True if len(Plan.objects.filter(run__in=runs)) != 0 else False)
            context['letter'] = Letter(run.section.wellbore.well_name)

    if request.method == 'POST':
        run = Run.objects.get(id=request.GET.get('run_id'))

        if 'plan_depth' in request.POST:  # данные с модальной формы 2 (плановая траектория)
            work_with_plan(request, run)

        if 'data-depth' in request.POST:  # данные с модальной формы 1 (добавление значенией)
            depth_data = request.POST['data-depth'].replace(',', '.').replace(' ', '') \
                .replace('\r', '').replace('\n', '\t').split('\t')
            corner_data = request.POST['data-corner'].replace(',', '.').replace(' ', '') \
                .replace('\r', '').replace('\n', '\t').split('\t')
            azimut_data = request.POST['data-azimut'].replace(',', '.').replace(' ', '') \
                .replace('\r', '').replace('\n', '\t').split('\t')

            if request.POST.get("data-type") == 'ННБ':
                obj = StaticNNBData.objects
            else:
                obj = IgirgiStatic.objects
            for meas in zip(depth_data, corner_data, azimut_data):
                if meas[0] != '' and meas[1] != '' and meas[2] != '':  # Если значения не нулевые
                    new_obj = obj.get_or_create(run=run, depth=meas[0])
                    new_obj[0].corner = meas[1]
                    new_obj[0].azimut = meas[2]
                    new_obj[0].save()

        return redirect(request.META.get('HTTP_REFERER'))  # вернуть на ту же страницу где и были
    return render(request, 'data_handler/trajectories.html', {'context': context, })


def edit_traj(request):
    """Страница с редактированием траекторией ННБ и ИГиРГИ"""
    context = {"title": 'Траектория',
               "active": 'traj',
               "tree": get_tree(),
               "igirgi_data": range(100),
               "nnb_data": range(100),
               }

    run_id = request.GET.get('run_id')

    if request.method == "GET":
        run = Run.objects.get(id=request.GET.get('run_id'))
        context['selected_obj'] = str(run)
        context['selected_id'] = run_id
        selected_for_tree(context, run)  # для раскрытия списка
        context["igirgi_data"] = IgirgiStatic.objects.filter(run=run_id)
        context["nnb_data"] = StaticNNBData.objects.filter(run=run_id)

    if request.method == 'POST':
        for items in request.POST.lists():
            key = str(items[0]).split(' ')
            # print(key)
            if 'nnb' in key:
                obj = StaticNNBData.objects.get(id=key[0])
            else:
                obj = IgirgiStatic.objects.get(id=key[0])
            # print(items[1]) - все 3 числа замеров
            if items[1][0] == '' or items[1][1] == '' or items[1][2] == '':
                obj.delete()
            else:
                obj.depth = float(items[1][0])
                obj.corner = float(items[1][1])
                obj.azimut = float(items[1][2])
                obj.save()

        context['selected_obj'] = str(Run.objects.get(id=run_id))
        context['selected_id'] = run_id
        context["igirgi_data"] = IgirgiStatic.objects.filter(run=run_id)
        context["nnb_data"] = StaticNNBData.objects.filter(run=run_id)
        return redirect('traj')
    return render(request, 'data_handler/edit_trajectories.html', {'context': context, })


def param(request):
    """Страница с параметрами"""
    context = {"title": 'Параметры',
               "active": 'param',
               "tree": get_tree(),
               }
    if request.method == "GET":
        if request.GET.get('run_id') is not None:
            run_id = request.GET.get('run_id')
            run = Run.objects.get(id=request.GET.get('run_id'))
            context['selected_obj'] = str(run)
            context['selected_id'] = run_id
            selected_for_tree(context, run)  # для раскрытия списка

    return render(request, 'data_handler/param.html', {'context': context, })


def graph(request):
    """Страница с графиком первичного контроля"""
    selected = dict()
    selected["well"] = 'None'
    depthGoxy = []
    depthGz = []
    depthGtotal = []
    depthGref = []
    depthGmax = []
    depthGmin = []
    depthBoxy = []
    depthBz = []
    depthBtotal = []
    depthBref = []
    depthBmax = []
    depthBmin = []
    depthBcorr = []  # пока нет функционала для Bcorr, временно берем Btotal
    depthDipraw = []
    depthDipref = []
    depthDipmax = []
    depthDipmin = []
    depthDipcorr = []  # пока нет функционала для Dipcorr, временно берем Dipraw
    depthHSTF = []
    if request.method == 'POST':
        well = Well.objects.get(id=request.POST['well'])
        runs = Run.objects.filter(section__wellbore__well_name=well)
        selected["well"] = str(well)  # для отображения на странице
        selected["id"] = request.POST['well']
        for run in runs:
            surveys = Data.objects.filter(run=run)
            for survey in surveys:
                # График Goxy-Gz
                depthGoxy.append({'x': survey.depth, 'y': survey.get_goxy()})
                depthGz.append({'x': survey.depth, 'y': survey.CZ})
                # График Gtotal
                depthGtotal.append({'x': survey.depth, 'y': survey.Gtotal()})
                depthGref.append({'x': survey.depth, 'y': well.gtotal})
                depthGmax.append({'x': survey.depth, 'y': well.max_gtotal()})
                depthGmin.append({'x': survey.depth, 'y': well.min_gtotal()})
                # График Boxy-Bz
                depthBoxy.append({'x': survey.depth, 'y': survey.get_boxy()})
                depthBz.append({'x': survey.depth, 'y': survey.BZ})
                # График Btotal
                depthBtotal.append({'x': survey.depth, 'y': survey.Btotal()})
                depthBref.append({'x': survey.depth, 'y': well.btotal})
                depthBmax.append({'x': survey.depth, 'y': well.max_btotal()})
                depthBmin.append({'x': survey.depth, 'y': well.min_btotal()})
                depthBcorr.append({'x': survey.depth, 'y': survey.Btotal_corr})
                # График HSTF
                depthHSTF.append({'x': survey.depth, 'y': survey.get_hstf()})
                # График Dip
                depthDipraw.append({'x': survey.depth, 'y': survey.Dip()})
                depthDipref.append({'x': survey.depth, 'y': well.dip})
                depthDipmax.append({'x': survey.depth, 'y': well.max_dip()})
                depthDipmin.append({'x': survey.depth, 'y': well.min_dip()})
                depthDipcorr.append({'x': survey.depth, 'y': survey.DIP_corr})

    try:
        firstDepth = depthHSTF[0]['x']
        lastDepth = depthHSTF[-1]['x']
    except IndexError:
        firstDepth = lastDepth = 0

    context = {
        'title': 'Контроль качества',
        'well': get_all_well(),
        "active": 'graph',
        'depthGoxy': depthGoxy,
        'depthGz': depthGz,
        'depthGtotal': depthGtotal,
        'depthGref': depthGref,
        'depthGmax': depthGmax,
        'depthGmin': depthGmin,
        'depthBoxy': depthBoxy,
        'depthBz': depthBz,
        'depthBtotal': depthBtotal,
        'depthBref': depthBref,
        'depthBmax': depthBmax,
        'depthBmin': depthBmin,
        'depthBcorr': depthBcorr,
        'depthDipraw': depthDipraw,
        'depthDipref': depthDipref,
        'depthDipmax': depthDipmax,
        'depthDipmin': depthDipmin,
        'depthDipcorr': depthDipcorr,
        'depthHSTF': depthHSTF,
        'firstDepth': firstDepth,
        'lastDepth': lastDepth,
        'selected': selected,
    }

    return render(request, 'data_handler/graph.html', {'context': context, })
