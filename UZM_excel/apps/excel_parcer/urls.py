from django.urls import path

from . import views

urlpatterns = [
    path('add', views.file, name="add_data"),
    path('', views.index, name='data'),
    path('run_index', views.get_run_index, name='run_index'),  # надо оформить как api
]
