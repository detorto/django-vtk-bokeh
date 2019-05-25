from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls import include
from app_vtk import views as vtkjs_views
from django.conf import settings

urlpatterns = [
    url(r'^json/$', vtkjs_views.vtkjs_json),
    url(r'^id/(?P<vtkjs_id>\d+)/data/',vtkjs_views.vtkjs_data),

    url(r'^$',vtkjs_views.vtkjs_index),
    url(r'^form/$',vtkjs_views.vtkjs_form),
    url(r'^id/(?P<vtkjs_id>\d+)/$', vtkjs_views.vtkjs_model),
]
