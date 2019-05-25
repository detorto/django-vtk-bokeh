from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls import include
from app_bokeh import views as bokeh_views
from django.conf import settings

urlpatterns = [
    url(r'^json/$',bokeh_views.bokeh_json),
    url(r'^id/(?P<bokeh_id>\d+)/image/$',bokeh_views.bokeh_image),
    url(r'^id/(?P<bokeh_id>\d+)/data/$',bokeh_views.data),

    url(r'^$',bokeh_views.bokeh_index),
    url(r'^form/$',bokeh_views.bokeh_form),
    url(r'^id/(?P<bokeh_id>\d+)/$', bokeh_views.bokeh_model),
]
