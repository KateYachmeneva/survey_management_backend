from django.urls import path, include

from . import views, views_api
from .views_api import *
from rest_framework import routers


urlpatterns = [
    path('api/meas/run/<int:run_pk>/', DataByRunAPIView.as_view()),
    path('api/meas/<int:pk>/', DataViewSet.as_view({'get': 'retrieve', 'post': 'create', 'put': 'update',
                                                    'delete': 'destroy'})),
    path('', views.index, name='axes'),
    path('graph', views.graph, name='graph_axes'),
    path('add', views.file, name="add_axes"),
    path('edit', views.edit_index, name='edit_axes'),
    path('telesystem', views.add_Device, name='add_device'),
    path('run_index', views.get_run_index, name='run_index'),  # надо оформить как api
    path('api/device_del', views.del_Device, name='device_del'),
    path('api/meas_del', views.del_Meas, name='meas_del'),
    path('api/coef_device', views.get_coef_device, name='device_coef'),
    path('api/wellbore_copy', views_api.wellbore_copy)
]
