#coding: utf-8
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
import os
import shutil


def create_bokeh_directory(id):
    if not os.path.exists(settings.BOKEH_DIR+"/{}/".format(id)):
        os.makedirs(settings.BOKEH_DIR+"/{}/".format(id))
    return settings.BOKEH_DIR_RELATIVE+"/{}/".format(id)

img_type_choices = (('line','line'),('circle','circle'), ('image','image'))

class BokehVisual(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    width = models.IntegerField(default=800)
    height = models.IntegerField(default=600)
    use_wgl = models.BooleanField(default=0)
    img_type = models.CharField(max_length=150, choices=img_type_choices)
    path     = models.TextField()

    def save(self, *args, **kwargs):
        res = super(BokehVisual, self).save(*args, **kwargs)
        kwargs['force_insert'] = False
        self.path = create_bokeh_directory(self.id)
        res = super(BokehVisual, self).save(*args, **kwargs)
        return res

    def default_save(self, *args, **kwargs):
        res = super(BokehVisual, self).save(*args, **kwargs)
        return res

    def __unicode__(self):
        return self.title
