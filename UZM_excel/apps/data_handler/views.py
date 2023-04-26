from django.shortcuts import render

# Create your views here.


def index(request):
    """Главная страница для генератора отчетов"""

    context = {"title": 'Работа с данными',
               }

    if request.method == 'POST':
        pass

    return render(request, 'data_handler/index.html', {'context': context, })


def traj(request):
    context = {"title": 'Траектория',
               }

    if request.method == 'POST':
        pass

    return render(request, 'data_handler/trajectories.html', {'context': context, })

