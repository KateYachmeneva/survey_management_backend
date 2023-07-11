from django.http import JsonResponse
from rest_framework import generics, viewsets, mixins
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .models import *
from .serializer import *
from .serializerTree import Tree


class ClientAPIView(APIView):
    def get(self, request):
        clients = Client.objects.all()
        for c in clients:
            c.full_name = str(c)
        return Response(ClientSerializer(clients, many=True).data)

    # def post(self, request):
    #     serializers = ClientSerializer(data=request.data)
    #     serializers.is_valid(raise_exception=True)
    #     serializers.save()
    #     return Response({'post': serializers.data})


class WellByClient(APIView):
    """Получаем список скважин по id заказчика"""

    def get(self, request, client_pk):
        wells = Well.objects.filter(pad_name__field__client__id=client_pk)
        return Response(WellSerializer(wells, many=True).data)


class RunByWell(APIView):
    """Получаем список рейсов по id скважины"""

    def get(self, request, well_id):
        runs = Run.objects.filter(section__wellbore__well_name__id=well_id)
        return Response(RunSerializer(runs, many=True).data)


class SectionByWell(APIView):
    """Получаем список секций по id скважины"""

    def get(self, request, well_id):
        sections = Section.objects.filter(wellbore__well_name__id=well_id)
        return Response(SectionSerializer(sections, many=True).data)


class ContractorNnbAPIView(generics.ListCreateAPIView):
    queryset = ContractorNNB.objects.all()
    serializer_class = ContractorNNBSerializer


class ContractorDrillAPIView(generics.ListCreateAPIView):
    queryset = ContractorDrill.objects.all()
    serializer_class = ContractorDrillSerializer


class FieldApiView(generics.ListAPIView):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer


class PadApiView(generics.ListCreateAPIView):
    queryset = Pad.objects.all()
    serializer_class = PadSerializer


# Viewsets - все миксины с добавлением, удалением, редактированием, выбором
class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.all()
    serializer_class = RunSerializer


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer


class WellboreViewSet(viewsets.ModelViewSet):
    queryset = Wellbore.objects.all()
    serializer_class = WellboreSerializer
    permission_classes = [AllowAny]


class WellViewSet(viewsets.ModelViewSet):
    queryset = Well.objects.all()
    serializer_class = WellSerializer


class PadViewSet(viewsets.ModelViewSet):
    queryset = Pad.objects.all()
    serializer_class = PadSerializer


class FieldViewSet(viewsets.ModelViewSet):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer


class WellWithRunViewSet(mixins.RetrieveModelMixin,
                         mixins.ListModelMixin,
                         GenericViewSet):
    """
    Явная связь скважина-ствол-секция-рейс
    """
    queryset = Well.objects.all()
    serializer_class = WellWithRunSerializer


def get_tree() -> list:
    """ Дерево для меню """
    trees = Tree(Client.objects.all(), many=True).data
    return trees


# смежные api
def get_field_by_do(request):
    """Функция для фильтрации"""
    field_data = dict()
    for field in Field.objects.filter(client=request.POST.get("do_id")):
        field_data[field.id] = field.field_name
    return JsonResponse(field_data)


def get_pad_by_field(request):
    """Функция для фильтрации"""
    pad_data = dict()
    for pad in Pad.objects.filter(field=request.POST.get("field_id")):
        pad_data[pad.id] = pad.pad_name
    return JsonResponse(pad_data)
