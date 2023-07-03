from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from . import serializer
from .forms import *
from .models import Client
from UZM_excel.conf import server_ip


def add_contractor_nnb(request):
    form = AddContractorNNBForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
        return redirect(add_contractor_drill)

    context = {"title": 'Подрядчик',
               "form": form,
               "method": "add_contractor_nnb",
               "data": models.ContractorNNB.objects.all().values()}
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
               "data": models.ContractorDrill.objects.all().values()}
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
               "data": serializer.FieldnameSerializer(models.Field.objects.all(), many=True).data}
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
               "data": serializer.PadnameSerializer(models.Pad.objects.all(), many=True).data}
    return render(request, 'Field/addModal.html', {'context': context, })


def add_well(request):
    form = AddWellForm(request.POST)
    form.base_fields['mail_To'].help_text = 'Введите адреса черех ";"'
    form.base_fields['mail_Cc'].help_text = 'Введите адреса черех ";"'
    if request.method == 'POST':
        if form.data['latitude'] != '' or form.data['longtitude'] != '':  # Ввод КООРДИНАТЫ УСТЬЯ XX YY ZZ
            _mutable = form.data._mutable  # изменяем QueryDicts
            form.data._mutable = True
            try:
                lat_v = [float(idx) for idx in form.data['latitude'].replace(',', '.').split(' ')]
                form.data['latitude'] = (round(float(lat_v[0]) + float(lat_v[1]) / 60 + float(lat_v[2]) / 3600, 3)
                                         if len(lat_v) > 2 else float(lat_v[0]))

            except:
                form.data['latitude'] = ''

            try:
                long_v = [float(idx) for idx in form.data['longtitude'].replace(',', '.').split(' ')]
                form.data['longtitude'] = (round(float(long_v[0]) + float(long_v[1]) / 60 + float(long_v[2]) / 3600, 3)
                                           if len(long_v) > 2 else float(long_v[0]))
            except:
                form.data['longtitude'] = ''

            form.data._mutable = _mutable

        if form.is_valid():
            form.save()
        return redirect(add_wellbore)

    context = {"title": 'Скважина',
               "form": form,
               "method": "add_well",
               "server_ip": server_ip,
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
