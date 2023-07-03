import os

from django.http import JsonResponse, FileResponse
from django.shortcuts import render, redirect

# Create your views here.
from UZM_excel.conf import server_ip
from .function.api_func import get_index
from .function.model_service import get_data
from .function.work_with_Excel import write_data_in_Excel
from .function.work_with_data import rewrite_ReportIndex, work_with_file
from Field.models import get_all_run, Run


def index(request):
    """Главная страница для генератора отчетов"""

    context = {"title": 'Отчет',
               "run": get_all_run(),
               'server_ip': server_ip}

    if request.method == 'POST':
        index_id = rewrite_ReportIndex(request.POST.dict())  # перезапись индексов, получаем id текущего рейса
        igirgi_data = request.POST['igirgi_data'].replace(',', '.').replace(' ', '') \
            .replace('\r', '').replace('\n', '\t').split('\t')

        if len(igirgi_data) < 3:  # фиксируем отсутсвие ручного ввода
            igirgi_data = None

        return work_with_file(request=request,
                              run_id=request.POST.dict()['run'],
                              index_id=index_id,
                              igirgi_data=igirgi_data)

    return render(request, 'report/index.html', {'context': context, })


# report/api/run_index
def run_index(request):
    """Функция для fetch запроса"""
    if request.method == 'POST':
        return get_index(request)
    return JsonResponse({'Warning_Text': 'нужно обращение к post методу'})


# report/api/file_name
def report(request):
    """Делаем отчёт по имеющимся данным и отправляем его имя"""
    # по рейсу ищем все остальные рейсы скважины
    run = Run.objects.get(id=request.POST['run_id'])
    runs = Run.objects.filter(section__wellbore__well_name=run.section.wellbore.well_name)
    all_data = get_data(runs)
    file_name, waste = write_data_in_Excel(all_data, f'Единая_форма_отчета0.xlsx', 0, run)  # имя файла и отходы
    return JsonResponse({'file_name': file_name, 'waste': waste})


# report/api/get_file
def get_file(request):
    """Пролучаем файл по имени """
    print('Беру отчёт с сервера!')
    file_name = request.POST['name']
    file_dir = os.getcwd() + "\\files"
    return FileResponse(open(file_dir + "\\Report_out\\" + file_name, 'rb'))
