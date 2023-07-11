# Viewsets - все миксины с добавлением, удалением, редактированием, выбором
from rest_framework import viewsets

from .function.functions import new_measurements, write_to_bd
from .models import *
from .serializer import *
from django.http import JsonResponse
from rest_framework import generics, viewsets, mixins
from rest_framework.response import Response
from rest_framework.views import APIView

from Field.models import Run


class DataViewSet(viewsets.ModelViewSet):
    """Работа с осями"""
    queryset = Data.objects.all()
    serializer_class = DataSerializer


class DataByRunAPIView(APIView):
    """Получаем/заполняем замеры осей по id рейса"""

    def get(self, request, run_pk):
        measurement = Data.objects.filter(run=run_pk)
        return Response(DataSerializer(measurement, many=True).data)

    def post(self, request, run_pk):
        current_run = Run.objects.get(id=run_pk)
        if 'data-axes' in request.POST:  # Модальная форма с ОСЯМИ
            axes_data = request.POST['data-axes'].replace(',', '.').\
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


