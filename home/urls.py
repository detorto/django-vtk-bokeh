from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls import include
from home import views as home_views

urlpatterns = [
    url(r'^',home_views.index ),
]