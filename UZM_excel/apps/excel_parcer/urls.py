from django.urls import path

from . import views

urlpatterns = [
    path('add', views.file, name="add_axes"),
    path('', views.index, name='axes'),
    path('run_index', views.get_run_index, name='run_index'),  # надо оформить как api
    path('edit', views.edit_index, name='edit_axes')
]
