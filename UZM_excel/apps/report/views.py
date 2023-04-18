from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
# from .read_function import rewrite_ReportIndex, work_with_file
from .function.api_func import get_index
from .function.work_with_data import rewrite_ReportIndex, work_with_file
from Field.models import get_all_run


def index(request):
    """Главная страница для генератора отчетов"""

    context = {"title": 'Отчет',
               "run": get_all_run()}

    if request.method == 'POST':
        index_id = rewrite_ReportIndex(request.POST.dict())  # перезапись индексов, получаем id текущего рейса

        igirgi_data = request.POST['igirgi_data'].replace(',', '.').replace(' ', '')\
            .replace('\r', '').replace('\n', '\t').split('\t')

        if len(igirgi_data) < 3:  # фиксируем отсутсвие ручного ввода
            igirgi_data = None

        return work_with_file(request=request,
                              run_id=request.POST.dict()['run'],
                              index_id=index_id,
                              igirgi_data=igirgi_data)

    return render(request, 'report/index.html', {'context': context, })


def run_index(request):
    """Функция для fetch запроса"""
    if request.method == 'POST':
        # print(request.POST.get('run_title'))
        return get_index(request)
    return JsonResponse({'Warning_Text': 'нужно обращение к post методу'})



