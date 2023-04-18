from rest_framework import generics, viewsets, mixins
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .models import *
from .serializer import *


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
