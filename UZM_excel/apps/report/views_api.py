# Viewsets - все миксины с добавлением, удалением, редактированием, выбором
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from .models import *
from .serializer import *
from django.http import JsonResponse
from rest_framework import generics, viewsets, mixins
from rest_framework.response import Response
from rest_framework.views import APIView

from Field.models import Run, Wellbore


class FileIndexView(APIView):
    """ Индексы для чтения траектории ННБ/ИГиРГИ/Плановой/Динамической/Сырой"""
    @swagger_auto_schema(tags=['Чтение файлов'],
                         operation_summary="Получить индексы для чтения файлов с траекторие",
                         request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             properties={
                                 'run_id': openapi.Schema(type=openapi.TYPE_NUMBER, description='id рейса'),
                             }
                         ),
                         responses={200: openapi.Response('response description', ReportIndexSerializer)},
                         )
    def post(self, request):
        try:
            run_id = request.POST.get('run_id')
            if run_id != "Выберите рейс":
                obj = Run.objects.get(id=run_id)
                report_index = ReportIndex.objects.get(run=obj)
                return Response(ReportIndexSerializer(report_index).data)
        except ReportIndex.DoesNotExist:
            pass
        except Run.DoesNotExist:
            pass
        return Response(ReportIndexSerializer().data)


class ProjectionParamView(APIView):
    """ Представления для работы с моделью параметров проекции, обрабатываем ProjectionParam """

    @swagger_auto_schema(tags=['Проекция'],
                         operation_summary="Записать параметры для постройки проекции",
                         request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             properties={
                                 'hor_x_min': openapi.Schema(type=openapi.TYPE_NUMBER,
                                                             description='горизонтальная проекция,'
                                                                         ' X минимальное (Запад/Восток)'),
                                 'hor_x_max': openapi.Schema(type=openapi.TYPE_NUMBER,
                                                             description='горизонтальная проекция,'
                                                                         ' X максимальное (Запад/Восток)'),
                                 'hor_x_del': openapi.Schema(type=openapi.TYPE_NUMBER,
                                                             description='горизонтальная проекция,'
                                                                         ' X шаг (Запад/Восток)'),
                                 'hor_y_min': openapi.Schema(type=openapi.TYPE_NUMBER,
                                                             description='горизонтальная проекция,'
                                                                         ' Y минимальное (Юг/Север)'),
                                 'hor_y_max': openapi.Schema(type=openapi.TYPE_NUMBER,
                                                             description='горизонтальная проекция,'
                                                                         ' Y максимальное (Юг/Север)'),
                                 'hor_y_del': openapi.Schema(type=openapi.TYPE_NUMBER,
                                                             description='горизонтальная проекция,'
                                                                         ' Y шаг (Юг/Север)'),
                                 'ver_x_min': openapi.Schema(type=openapi.TYPE_NUMBER,
                                                             description='вертикальная проекция,'
                                                                         ' X минимальное (Вертикальная секция)'),
                                 'ver_x_max': openapi.Schema(type=openapi.TYPE_NUMBER,
                                                             description='вертикальная проекция,'
                                                                         ' X максимальное (Вертикальная секция)'),
                                 'ver_x_del': openapi.Schema(type=openapi.TYPE_NUMBER,
                                                             description='вертикальная проекция,'
                                                                         ' X шаг (Вертикальная секция)'),
                                 'ver_y_min': openapi.Schema(type=openapi.TYPE_NUMBER,
                                                             description='вертикальная проекция,'
                                                                         ' Y минимальное (Абсолютная отметка)'),
                                 'ver_y_max': openapi.Schema(type=openapi.TYPE_NUMBER,
                                                             description='вертикальная проекция,'
                                                                         ' Y максимальное (Абсолютная отметка)'),
                                 'ver_y_del': openapi.Schema(type=openapi.TYPE_NUMBER,
                                                             description='вертикальная проекция,'
                                                                         ' Y шаг (Абсолютная отметка)'),

                             }
                         )
                         )
    def post(self, request, wellbore_id):
        if wellbore_id is None:
            return Response({'warning': 'Не указан id ствола! Укажите id в параметре wellbore_id.'})
        else:
            try:
                w = Wellbore.objects.get(id=wellbore_id)
            except Exception as e:
                return Response({'warning': 'Ствол с указанным id не существует!'})

        obj = ProjectionParam.objects.get_or_create(wellbore=w)
        print(request.POST.dict())
        # проверка на наличие коэффициентов
        hor = True
        ver = True
        hor_x_min = request.POST.get('hor_x_min')
        hor_x_max = request.POST.get('hor_x_max')
        hor_x_del = request.POST.get('hor_x_del')
        hor_y_min = request.POST.get('hor_y_min')
        hor_y_max = request.POST.get('hor_y_max')
        hor_y_del = request.POST.get('hor_y_del')

        if None or '' in (hor_x_min, hor_x_max, hor_x_del, hor_y_min, hor_y_max, hor_y_del):
            hor = False
        else:
            obj[0].hor_x_min = hor_x_min
            obj[0].hor_x_max = hor_x_max
            obj[0].hor_x_del = hor_x_del
            obj[0].hor_y_min = hor_y_min
            obj[0].hor_y_max = hor_y_max
            obj[0].hor_y_del = hor_y_del

        ver_x_min = request.POST.get('ver_x_min')
        ver_x_max = request.POST.get('ver_x_max')
        ver_x_del = request.POST.get('ver_x_del')
        ver_y_min = request.POST.get('ver_y_min')
        ver_y_max = request.POST.get('ver_y_max')
        ver_y_del = request.POST.get('ver_y_del')

        if None or '' in (ver_x_min, ver_x_max, ver_x_del, ver_y_min, ver_y_max, ver_y_del):
            ver = False
        else:
            obj[0].ver_x_min = ver_x_min
            obj[0].ver_x_max = ver_x_max
            obj[0].ver_x_del = ver_x_del
            obj[0].ver_y_min = ver_y_min
            obj[0].ver_y_max = ver_y_max
            obj[0].ver_y_del = ver_y_del

        if not ver and not hor:
            return Response({'warning': 'Не заполнены обязательные параметры!'})

        print(obj)
        obj[0].save()
        return Response({'status': 'ок'})

    @swagger_auto_schema(tags=['Проекция'],
                         operation_summary="Получить параметры для постройки проекции по id ствола", )
    def get(self, request, wellbore_id):
        try:
            params = ProjectionParam.objects.get(wellbore=wellbore_id)
            return Response(ProjectionParamSerializer(params).data)
        except:
            return Response({'warning': 'Не удалось найти параметры по данному id ствола.'})
