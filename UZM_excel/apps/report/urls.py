from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='report'),
    path('api/run_index', views.run_index, name='run_index'),
    path('api/file_name', views.report, name='get_file_name'),
    path('api/get_file', views.get_file, name='get_file'),
    # path('api/delete_igirgi_data', views.delete_igirgi_data, name='delete_igirgi_data'),
    # path('data_input/', views.manual_input, name='manual_input'),
]
