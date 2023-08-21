from django.urls import path

from . import views

# Точки для работы с моделями траектории [обращаемся с DjangoTemplate по fetch запросу]
urlpatterns = [
    # path('', views.index, name='report'),
    path('api/run_index', views.run_index, name='run_index'),
    path('api/update_index', views.update_index),
    path('api/file_name', views.report, name='get_file_name'),
    path('api/get_file', views.get_report_file, name='get_report_file'),
    path('api/plan_del', views.plan_del, name='plan_del'),
    path('api/wellbore_copy', views.wellbore_copy, name='clone'),
    path('api/meas_del', views.traj_del, name='traj_del'),
    path('api/traj_comm', views.put_comment),
    path('api/graph', views.get_graph),
    path('api/upload_file', views.uploadFile),  # внутри смотрим на то какой файл нам пришел
    # path('api/delete_igirgi_data', views.delete_igirgi_data, name='delete_igirgi_data'),
    # path('data_input/', views.manual_input, name='manual_input'),
    path('api/comment_copy', views.comment_copy)
]
