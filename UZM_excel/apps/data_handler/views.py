from django.shortcuts import render

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


def graph(request):
    """Страница с графиками"""
    context = {"title": 'График',
               "active": 'graph',
               }
    return render(request, 'data_handler/graph.html', {'context': context, })


def param(request):
    """Страница с параметрами"""
    context = {"title": 'Параметры',
               "active": 'param',
               }
    return render(request, 'data_handler/param.html', {'context': context, })

