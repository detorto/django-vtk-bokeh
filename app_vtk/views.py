# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
import os
import json
from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to
from django.http import JsonResponse
from django.core import serializers
from django.http import HttpResponse

from .models import VtkjsVisual
from .forms import VtkjsVisualForm


def vtkjs_json(request):
    visuals = {}
    if request.method == "GET":
        bokeh_id = request.GET.get('vtkjs_id',None)
        if bokeh_id:
            models = VtkjsVisual.objects.get(pk=bokeh_id)
            visuals['get'] = json.loads(serializers.serialize('json', [models,]))
        else:
            models = VtkjsVisual.objects.all()
            visuals['get'] = json.loads(serializers.serialize('json', models))
    else:
        form = VtkjsVisualForm(request.POST, request.FILES)
        if form.is_valid():
            models = VtkjsVisual.objects.create()
            models.title = form.cleaned_data['title']
            models.description = form.cleaned_data['description']
            models.width = form.cleaned_data['width']
            models.height = form.cleaned_data['height']
            models.save()
            with open(os.path.join(models.path,'vis.dat'),'w') as f_out:
                f_out.write(form.cleaned_data['inputfile'].read())
            visuals['get'] = json.loads(serializers.serialize('json', [models,]))
        else:
            visuals['form_error'] = form.errors
    return JsonResponse(visuals)

import xml_helper as xmlh
import vtk
def vtkjs_data(request,vtkjs_id):
    models = VtkjsVisual.objects.get(pk=vtkjs_id)
    with open('{}/vis.dat'.format(models.path),'rb') as f_vis:
        data = f_vis.read()
    resp = HttpResponse(data, content_type='application/force-download')
    resp['Content-Disposition'] = 'inline; filename="vis.dat"'
    return resp

@render_to('vtk_js_index.html')
def vtkjs_index(request):
    return {"user":request.user, "current":"vtkjs"}

@render_to('vtk_js_visual.html')
def vtkjs_model(request, vtkjs_id):
    return {"user":request.user, "current":"vtkjs", "vtkjs_id":vtkjs_id}

@render_to('vtk_js_create.html')
def vtkjs_form(request):
    form = VtkjsVisualForm()
    return {"user":request.user, 'form': form, "current":"vtkjs"}
