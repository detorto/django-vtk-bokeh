# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
import os
import shutil


def create_vtkjs_directory(id):
    if not os.path.exists(settings.VTK_DIR+"/{}/".format(id)):
        os.makedirs(settings.VTK_DIR+"/{}/".format(id))
    return settings.VTK_DIR_RELATIVE+"/{}/".format(id)

class VtkjsVisual(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    width = models.IntegerField(default=800)
    height = models.IntegerField(default=600)
    path     = models.TextField()

    def save(self, *args, **kwargs):
        res = super(VtkjsVisual, self).save(*args, **kwargs)
        kwargs['force_insert'] = False
        self.path = create_vtkjs_directory(self.id)
        res = super(VtkjsVisual, self).save(*args, **kwargs)
        return res

    def default_save(self, *args, **kwargs):
        res = super(VtkjsVisual, self).save(*args, **kwargs)
        return res

    def __unicode__(self):
        return self.title
