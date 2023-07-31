from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from . import serializer
from .forms import *
from .models import *
from .serializer import ContractorNNBSerializer_Add, ContractorDrillSerializer_Add


def add_contractor_nnb(request):
    form = AddContractorNNBForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
        return redirect(add_contractor_drill)

    context = {"title": 'Подрядчик',
               "form": form,
               "method": "add_contractor_nnb",
               "data": ContractorNNBSerializer_Add(ContractorNNB.objects.all(), many=True).data}
    return render(request, 'Field/addModal.html', {'context': context, })


def add_contractor_drill(request):
    form = AddContractorDrillForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
        return redirect(add_field)

    context = {"title": 'Подрядчик',
               "form": form,
               "method": "add_contractor_drill",
               "data": ContractorDrillSerializer_Add(ContractorDrill.objects.all(), many=True).data}
    return render(request, 'Field/addModal.html', {'context': context, })


def add_field(request):
    form = AddFieldForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
        return redirect(add_pad)

    context = {"title": 'Месторождение',
               "form": form,
               "method": "add_field",
               "data": serializer.FieldnameSerializer(Field.objects.all(), many=True).data}
    return render(request, 'Field/addModal.html', {'context': context, })


def add_pad(request):
    form = AddPadForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
        return redirect(add_well)

    context = {"title": 'Куст',
               "form": form,
               "method": "add_pad",
               "data": serializer.PadnameSerializer(Pad.objects.all(), many=True).data}
    return render(request, 'Field/addModal.html', {'context': context, })


def add_well(request):
    form = AddWellForm(request.POST)
    form.base_fields['mail_To'].help_text = 'Введите адреса черех ";"'
    form.base_fields['mail_Cc'].help_text = 'Введите адреса черех ";"'
    if request.method == 'POST':
        if form.is_valid():
            form.save()
        return redirect(add_wellbore)

    context = {"title": 'Скважина',
               "form": form,
               "method": "add_well",
               "DO": Client.objects.all()}

    return render(request, 'Field/addWell.html', {'context': context, })


def add_wellbore(request):
    form = AddWellboreForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
        return redirect(add_section)

    context = {"title": 'Ствол',
               "form": form,
               "method": "add_wellbore"}
    return render(request, 'Field/addModal.html', {'context': context, })


def add_section(request):
    form = AddSectionForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
        return redirect(add_run)

    context = {"title": 'Секция',
               "form": form,
               "method": "add_section"}
    return render(request, 'Field/addModal.html', {'context': context, })


def add_run(request):
    form = AddRunForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
        return redirect('empty_page')

    context = {"title": 'Рейс',
               "form": form,
               "method": "add_run"}
    return render(request, 'Field/addModal.html', {'context': context, })


def clone_wellbore(request):
    # print(request.POST)
    old_wellbore = Wellbore.objects.get(id=request.POST['wellbore_id'])
    new_wellbore = Wellbore.objects.create(well_name=old_wellbore.well_name, wellbore=request.POST['wellbore_name'])
    for old_section in Section.objects.filter(wellbore=old_wellbore):
        new_section = Section.objects.create(section=old_section.section, wellbore=new_wellbore,
                                             target_depth=old_section.target_depth)
        for old_run in Run.objects.filter(section=old_section):
            new_run = Run.objects.create(run_number=old_run.run_number, section=new_section,
                                         start_date=old_run.start_date,
                                         end_date=old_run.end_date,
                                         start_depth=old_run.start_depth,
                                         end_depth=old_run.end_depth,
                                         in_statistics=old_run.in_statistics,
                                         memory=old_run.memory,
                                         bha=old_run.bha,
                                         sag=old_run.sag,
                                         dd_contractor_name=old_run.dd_contractor_name)

    return JsonResponse({'old_wellbore': old_wellbore.id, 'new_wellbore': new_wellbore.id})
