from django.urls import path

from . import views

urlpatterns = [
    path('add', views.file, name="add_axes"),
    path('', views.index, name='axes'),
    path('run_index', views.get_run_index, name='run_index'),  # надо оформить как api
    path('edit', views.edit_index, name='edit_axes'),
    path('telesystem', views.add_Device, name='add_device'),
    path('api/device_del', views.del_Device, name='device_del'),
    path('api/coef_device', views.get_coef_device, name='device_coef')
]
