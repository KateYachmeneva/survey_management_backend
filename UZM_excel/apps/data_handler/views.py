from django.shortcuts import render
from Field.models import Well, Run, get_all_well
from excel_parcer.models import Data
# Create your views here.


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
               "igirgi_data": range(100),
               "nnb_data": range(100),
               }

    if request.method == 'POST':

        pass

    return render(request, 'data_handler/trajectories.html', {'context': context, })


def param(request):
    """Страница с параметрами"""
    context = {"title": 'Параметры',
               "active": 'param',
               }
    return render(request, 'data_handler/param.html', {'context': context, })


def graph(request):
    """Страница с графиком первичного контроля"""
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
                depthBcorr.append({'x': survey.depth, 'y': survey.Btotal()})
                # График HSTF
                depthHSTF.append({'x': survey.depth, 'y': survey.get_hstf()})
                # График Dip
                depthDipraw.append({'x': survey.depth, 'y': survey.Dip()})
                depthDipref.append({'x': survey.depth, 'y': well.dip})
                depthDipmax.append({'x': survey.depth, 'y': well.max_dip()})
                depthDipmin.append({'x': survey.depth, 'y': well.min_dip()})
                depthDipcorr.append({'x': survey.depth, 'y': survey.Dip()})

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
    }

    return render(request, 'data_handler/graph.html', {'context': context, })