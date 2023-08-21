# Viewsets - все миксины с добавлением, удалением, редактированием, выбором
from django.utils.decorators import method_decorator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from .function.functions import new_measurements, write_to_bd
from .function.model_service import clone_wellbore_axes
from .models import *
from .serializer import *
from django.http import JsonResponse
from rest_framework import generics, viewsets, mixins
from rest_framework.response import Response
from rest_framework.views import APIView

from Field.models import Run


class TelesystemCoefApiView(APIView):
    """ Коэффициенты телесистемы """

    @swagger_auto_schema(tags=['Телесистема'],
                         operation_summary="Получить коэффициенты телесистемы по id рейса", )
    def get(self, request, run_id):
        try:
            d = TelesystemIndex.objects.get(run=run_id).device
            return JsonResponse({'device_title': d.device_title,
                                 'CX': d.CX,
                                 'CY': d.CY,
                                 'CZ': d.CZ,
                                 'BX': d.BX,
                                 'BY': d.BY,
                                 'BZ': d.BZ})
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'Коэффициенты не найдены'})

    @swagger_auto_schema(tags=['Телесистема'],
                         operation_summary="Записать коэффициенты телесистемы",
                         request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             properties={
                                 'device_title': openapi.Schema(type=openapi.TYPE_STRING, description='Наименование'),
                                 'CX': openapi.Schema(type=openapi.TYPE_STRING, description='Коэф. GX'),
                                 'CY': openapi.Schema(type=openapi.TYPE_STRING, description='Коэф. GY'),
                                 'CZ': openapi.Schema(type=openapi.TYPE_STRING, description='Коэф. GZ'),
                                 'BX': openapi.Schema(type=openapi.TYPE_STRING, description='Коэф. BX'),
                                 'BY': openapi.Schema(type=openapi.TYPE_STRING, description='Коэф. BY'),
                                 'BZ': openapi.Schema(type=openapi.TYPE_STRING, description='Коэф. BZ'),
                             }
                         ),
                         Response={200: 'Коэффициенты записаны'}
                         )
    def post(self, request, run_id):
        print(request.POST.dict())
        try:
            run = Run.objects.get(id=run_id)
        except:
            return JsonResponse({'status': f'Рейс с id {run_id} не найден'})
        t = TelesystemIndex.objects.get_or_create(run=run)
        if t[0].device is None:
            d = Device.objects.create(device_title=request.POST['device_title'],
                                      CX=request.POST['CX'],
                                      CY=request.POST['CY'],
                                      CZ=request.POST['CZ'],
                                      BX=request.POST['BX'],
                                      BY=request.POST['BY'],
                                      BZ=request.POST['BZ'])
            d.save()
            t[0].device = d
            t[0].save()
        else:
            t[0].device.device_title = request.POST.get('device_title')
            t[0].device.CX = request.POST.get('CX')
            t[0].device.CY = request.POST.get('CY')
            t[0].device.CZ = request.POST.get('CZ')
            t[0].device.BX = request.POST.get('BX')
            t[0].device.BY = request.POST.get('BY')
            t[0].device.BZ = request.POST.get('BZ')
            t[0].device.save()

        return request


@method_decorator(name='create',
                  decorator=swagger_auto_schema(tags=['Оси'], operation_summary="Добавить замер"))
@method_decorator(name='update',
                  decorator=swagger_auto_schema(tags=['Оси'], operation_summary="Обновить данные замера по id"))
@method_decorator(name='destroy',
                  decorator=swagger_auto_schema(tags=['Оси'], operation_summary="Удалить данные замера по id"))
@method_decorator(name='retrieve',
                  decorator=swagger_auto_schema(tags=['Оси'], operation_summary="Получить данные замера по id"))
class DataViewSet(viewsets.ModelViewSet):
    """Работа с осями"""
    queryset = Data.objects.all()
    serializer_class = DataSerializer


class DataByRunAPIView(APIView):
    """Получаем/заполняем замеры осей по id рейса"""

    @swagger_auto_schema(tags=['Оси'],
                         operation_summary="Получить все замеры по id рейса")
    def get(self, request, run_id):
        measurement = Data.objects.filter(run=run_id)
        return Response(DataSerializer(measurement, many=True).data)

    @swagger_auto_schema(tags=['Оси'],
                         operation_summary="Записать новые замеры по id рейса",
                         request_body=openapi.Schema(
                             type=openapi.TYPE_OBJECT,
                             properties={
                                 'data-axes': openapi.Schema(type=openapi.TYPE_STRING, description='Текстовое поле для'
                                                                                                   ' вставки осей'),
                             }
                         )
                         )
    def post(self, request, run_id):
        current_run = Run.objects.get(id=run_id)
        if 'data-axes' in request.POST:  # Модальная форма с ОСЯМИ
            axes_data = request.POST['data-axes'].replace(',', '.'). \
                replace(' ', '').replace('\r', '').replace('\n', '\t').split('\t')
            counter = 0
            manually_bz = list()
            manually_by = list()
            manually_bx = list()
            manually_gz = list()
            manually_gy = list()
            manually_gx = list()
            manually_depth = list()
            for data in axes_data:
                if data == '':
                    continue
                if counter == 0:
                    manually_depth.append(data)
                elif counter == 1:
                    manually_gx.append(data)
                elif counter == 2:
                    manually_gy.append(data)
                elif counter == 3:
                    manually_gz.append(data)
                elif counter == 4:
                    manually_bx.append(data)
                elif counter == 5:
                    manually_by.append(data)
                else:
                    manually_bz.append(data)
                counter = (0 if counter == 6 else counter + 1)
            # result - считанные данные
            result = zip(manually_depth, manually_gx, manually_gy, manually_gz, manually_bx, manually_by, manually_bz)
            if request.POST.get('device') != '-----':
                result2 = new_measurements(list(result), request.POST.get('device'))  # перобразованные данные
                write_to_bd(result2, current_run)
            else:
                write_to_bd(result, current_run)
        return JsonResponse({'status': 'good'})


# axes/api/wellbore_copy
def wellbore_copy(request):
    """ По fetch запросу с клиента клонируются замеры ствола c осями
    (в request должны лежать id нового и старого стволов, сама модель Wellbore создается в модуле Field заранее)"""
    clone_wellbore_axes(request)
    return JsonResponse({'status': 'ok'})
