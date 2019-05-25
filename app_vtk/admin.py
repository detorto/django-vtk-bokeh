# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from .models import VtkjsVisual


class VtkjsAdmin(admin.ModelAdmin):
    models = VtkjsVisual

admin.site.register(VtkjsVisual, VtkjsAdmin)
