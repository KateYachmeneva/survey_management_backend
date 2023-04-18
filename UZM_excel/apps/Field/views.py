from django.shortcuts import render, redirect

# Create your views here.
from . import serializer
from .forms import *


def add_contractor_nnb(request):
    form = AddContractorNNBForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
        return redirect(add_contractor_drill)

    context = {"title": 'Подрятчик',
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

    context = {"title": 'Подрятчик',
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
    if request.method == 'POST':
        if form.is_valid():
            form.save()
        return redirect(add_wellbore)

    context = {"title": 'Скважина',
               "form": form,
               "method": "add_well"}

    return render(request, 'Field/addModal.html', {'context': context, })


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
