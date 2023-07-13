from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='report'),
    path('api/run_index', views.run_index, name='run_index'),
    path('api/file_name', views.report, name='get_file_name'),
    path('api/get_file', views.get_file, name='get_file'),
    path('api/plan_del', views.plan_del, name='plan_del'),
    path('api/wellbore_copy', views.wellbore_copy, name='clone'),
    path('api/meas_del', views.traj_del, name='traj_del')
    # path('api/delete_igirgi_data', views.delete_igirgi_data, name='delete_igirgi_data'),
    # path('data_input/', views.manual_input, name='manual_input'),
]
