from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='data_info'),
    path('trajectories', views.traj, name='traj'),
    path('trajectories', views.traj, name='traj'),
    path('trajectories', views.traj, name='traj'),

]
