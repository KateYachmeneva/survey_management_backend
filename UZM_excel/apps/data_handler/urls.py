from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='data_info'),
    path('graph', views.graph, name='graph'),
    path('parametrs', views.param, name='param'),
    path('trajectories', views.traj, name='traj'),
    path('edit_trajectories/<int:run_id>', views.edit_traj, name='edit_traj'),


]
