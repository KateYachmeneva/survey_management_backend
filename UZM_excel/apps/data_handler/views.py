from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from pytest import console_main
from Field.models import Well, Run, Wellbore, Section
from excel_parcer.models import Data
from report.models import StaticNNBData, IgirgiStatic, Plan
from report.function.work_with_data import work_with_plan
from Field.views_api import get_tree
from .function.context_editer import *
from .function.mail import *
from report.function.model_service import waste

from Field.forms import AddWellForm


def index(request):
    """Главная страница"""
    context = {"title": 'Работа с данными',
               }
    return render(request, 'data_handler/index.html', {'context': context, })


def traj(request):
    """Страница с траекторией ННБ и ИГиРГИ"""
    context = {"title": 'Траектория', "active": 'traj',
               "tree": get_tree(), }

    if request.method == "GET":
        if request.GET.get('run_id') is not None:  # если в get запросе не run_id выводим пустую страницу
            run_id = request.GET.get('run_id')
            try:
                run = Run.objects.get(id=run_id)
            except:  # если не нашли рейс возвращаем пустую страницу
                return render(request, 'data_handler/trajectories.html', {'context': context, })
            selected_for_tree(context, run)  # для раскрытия списка

            context['selected_obj'] = str(run)  # для отображения текущей модели на странице (текст)
            context['selected_id'] = run_id  # для перенаправления по id на редактирование

            # Замеры
            context["igirgi_data"] = IgirgiStatic.objects.filter(run=run_id)
            context["nnb_data"] = StaticNNBData.objects.filter(run=run_id)
            # Отходы
            context["waste_hor"], context["waste_vert"], context["waste_common"] = waste(run.section.wellbore, 1)
            # Индексы отходов (Какие отходы выводить)
            context["waste_index"] = list()
            for ind, data in enumerate(IgirgiStatic.objects.filter(
                    run__section__wellbore=run.section.wellbore).order_by('depth')):
                if data in context['igirgi_data'] and ind < len(StaticNNBData.objects.filter(
                        run__section__wellbore=run.section.wellbore).order_by('depth')):
                    context["waste_index"].append(ind)

            # Ищем план, формируем контекст для письма
            runs = Run.objects.filter(section__wellbore=run.section.wellbore)
            plan_data = Plan.objects.filter(run__in=runs)
            context["plan_ex"] = (True if len(plan_data) != 0 else False)
            context["plan_version"] = (Plan.objects.filter(run__in=runs)[0].plan_version if context["plan_ex"] else
                                       '-')
            context['letter'] = Letter(run.section.wellbore)

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
    context = {"title": 'Параметры', "active": 'param',
               "tree": get_tree(),
               'cards': list(),  # карточки стволов
               }
    if request.GET.get('run_id') is not None:
        run_id = request.GET.get('run_id')
        try:  # можем удалить из страницы с run_id самого себя, поэтому если не нашли рейс отображаем пустую страницу
            run = Run.objects.get(id=request.GET.get('run_id'))
        except:
            context['form'] = AddWellForm()
            return render(request, 'data_handler/param.html', {'context': context, })
        # для работы с стволами
        context["wellbore_choices"] = run.section.wellbore.get_choices()
        context['selected_obj'] = run.section.wellbore.well_name
        # карточки с стволами
        for wellbore in Wellbore.objects.filter(well_name=run.section.wellbore.well_name):
            context['cards'].append(WellboreCard(wellbore))
    else:
        context['form'] = AddWellForm(request.POST)
        return render(request, 'data_handler/param.html', {'context': context, })

    context['form'] = AddWellForm(instance=run.section.wellbore.well_name)

    if request.method == 'POST':
        context['form'] = AddWellForm(request.POST, instance=run.section.wellbore.well_name)
        if context['form'].is_valid():
            context['form'].save()
        else:
            print(context['form'].errors.as_data())

    selected_for_tree(context, run)  # для раскрытия списка

    return render(request, 'data_handler/param.html', {'context': context, })


def plan(request):
    context = {'title': 'Плановая траектория',
               "tree": get_tree(),
               "active": 'plan', }

    if request.GET.get('run_id') is not None:
        try:  # проверка на существование рейса
            run = Run.objects.get(id=request.GET.get('run_id'))
            selected_for_tree(context, run)  # для раскрытия списка
        except:
            return render(request, 'data_handler/plan.html', {'context': context, })
        context['selected_obj'] = run

        # ищем план в БД
        for section in run.section.wellbore.sections.all():
            runs = section.runs.all()
            plan_meas = Plan.objects.filter(run__in=runs)
            if len(plan_meas) != 0:
                context['plan'] = plan_meas
                context["plan_ex"] = True
                context["plan_version"] = (Plan.objects.filter(run__in=runs)[0].plan_version if context["plan_ex"] else
                                           '-')
                break

    if request.method == 'POST':
        if 'plan_depth' in request.POST:  # данные с модальной формы 2 (плановая траектория)
            work_with_plan(request, run)

    return render(request, 'data_handler/plan.html', {'context': context, })


# TODO вытащить в сервисы
class WellboreCard:
    def __init__(self, wellbore):
        self.id = wellbore.id
        self.title = wellbore.get_full_wellbore_name
        runs = Run.objects.filter(section__wellbore=wellbore)
        self.section_len = Section.objects.filter(wellbore=wellbore).count()
        self.igirgi_len = IgirgiStatic.objects.filter(run__in=runs).count()
        self.nnb_len = StaticNNBData.objects.filter(run__in=runs).count()
