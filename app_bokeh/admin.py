# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import BokehVisual


class BokehAdmin(admin.ModelAdmin):
    models = BokehVisual

admin.site.register(BokehVisual, BokehAdmin)
