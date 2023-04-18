from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='report'),
    path('api/run_index', views.run_index, name='run_index'),
    # path('api/delete_igirgi_data', views.delete_igirgi_data, name='delete_igirgi_data'),
    # path('data_input/', views.manual_input, name='manual_input'),
]
