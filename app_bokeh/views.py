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

from .models import BokehVisual
from .forms import BokehVisualForm

from bokeh.plotting import figure, output_file, show
from bokeh.embed import components
from bokeh.models import AjaxDataSource, ColumnDataSource
import bokeh


def bokeh_json(request):
    visuals = {}
    if request.method == "GET":
        bokeh_id = request.GET.get('bokeh_id',None)
        if bokeh_id:
            models = BokehVisual.objects.get(pk=bokeh_id)
            visuals['get'] = json.loads(serializers.serialize('json', [models,]))
        else:
            models = BokehVisual.objects.all()
            visuals['get'] = json.loads(serializers.serialize('json', models))
    else:
        form = BokehVisualForm(request.POST, request.FILES)
        if form.is_valid():
            models = BokehVisual.objects.create()
            models.title = form.cleaned_data['title']
            models.description = form.cleaned_data['description']
            models.width = form.cleaned_data['width']
            models.height = form.cleaned_data['height']
            models.use_wgl = form.cleaned_data['use_wgl']
            models.img_type = form.cleaned_data['img_type']
            models.save()
            with open(os.path.join(models.path,'vis.dat'),'w') as f_out:
                f_out.write(form.cleaned_data['inputfile'].read())
            visuals['get'] = json.loads(serializers.serialize('json', [models,]))
        else:
            visuals['form_error'] = form.errors
    return JsonResponse(visuals)

def bokeh_image(request, bokeh_id):
    model = BokehVisual.objects.get(pk=bokeh_id)
    x_title = ""
    y_title = ""
    x = []
    y = []
    with open(os.path.join(model.path,'vis.dat'),'r') as f_in:
        titles = f_in.readline().split(',')
        x_title = titles[0].replace(' ','')
        y_title = titles[1].replace(' ','')
        for line in f_in:
            vals = line.split(',')
            x.append(float(vals[0]))
            y.append(float(vals[1]))

    source = ColumnDataSource(data={'x':x,'y':y})
    plot = figure(title= model.title,
                  x_axis_label= x_title,
                  y_axis_label= y_title,
                  plot_width = model.width,
                  plot_height = model.height)
    if model.use_wgl:
        plot = figure(title= model.title,
                      x_axis_label= x_title,
                      y_axis_label= y_title,
                      plot_width = model.width,
                      plot_height = model.height,
                      output_backend="webgl")
    else:
        plot = figure(title= model.title,
                      x_axis_label= x_title,
                      y_axis_label= y_title,
                      plot_width = model.width,
                      plot_height = model.height)

    if(model.img_type == 'line'):
        im = plot.line('x', 'y', source=source)
    if(model.img_type == 'circle'):
        im = plot.circle('x', 'y', source=source)

    callback = bokeh.models.CustomJS(args=dict(src=source,img=im, plt=plot), code="""
        var source = src;
        var image = img;
        var plot = plt;
        start_redrawing = Date.now();
        for (var i = 0; i < 100000; i++) {
            //plot.x_range.end += 0.0001;
            //image.change.emit();
            //plot.change.emit();
            source.change.emit();
        }
        stop_redrawing = Date.now();
        statistic_redrawing();
    """)
    button = bokeh.models.Button(label="Start redrawing", callback=callback)
    layout = bokeh.models.layouts.Column(button, plot)

    response_dict = {'script':'', 'div':''}
    response_dict['script'], response_dict['div'] = components(layout)
    return JsonResponse({'get':response_dict})


def data(request, bokeh_id):
    model = BokehVisual.objects.get(pk=bokeh_id)
    x = []
    y = []
    with open(os.path.join(model.path,'vis.dat'),'r') as f_in:
        titles = f_in.readline().split(',')
        for line in f_in:
            vals = line.split(',')
            x.append(float(vals[0]))
            y.append(float(vals[1]))
    return JsonResponse({'x':x,'y':y})


def bokeh_image_ajax_data(request, bokeh_id):
    model = BokehVisual.objects.get(pk=bokeh_id)
    x_title = ""
    y_title = ""
    with open(os.path.join(model.path,'vis.dat'),'r') as f_in:
        titles = f_in.readline().split(',')
        x_title = titles[0].replace(' ','')
        y_title = titles[1].replace(' ','')

    plot = figure(title= model.title,
                  x_axis_label= x_title,
                  y_axis_label= y_title,
                  plot_width = model.width,
                  plot_height = model.height)

    source = AjaxDataSource(data_url="http://localhost:8000/bokeh/id/{}/data/".format(bokeh_id), content_type="json", method="GET", mode='replace')
    source.data = dict(x=[], y=[])

    if(model.img_type == 'line'):
        im = plot.line('x', 'y', source=source)
    if(model.img_type == 'circle'):
        im = plot.circle('x', 'y', source=source)

    callback = bokeh.models.CustomJS(args=dict(src=source,plt=plot), code="""
        var source = src;
        var plot = plt;
        start_redrawing = Date.now();
        for (var i = 0; i < 100000; i++) {
            plot.change.emit();
        }
        stop_redrawing = Date.now();
        statistic_redrawing();
    """)
    button = bokeh.models.Button(label="Start redrawing", callback=callback)
    layout = bokeh.models.layouts.Column(button, plot)

    response_dict = {'script':'', 'div':''}
    response_dict['script'], response_dict['div'] = components(layout)
    return JsonResponse({'get':response_dict})



@render_to('bokeh_index.html')
def bokeh_index(request):
    return {"user":request.user, "current":"bokeh"}


@render_to('bokeh_visual.html')
def bokeh_model(request, bokeh_id):
    return {"user":request.user, "current":"bokeh", "bokeh_id":bokeh_id}


@render_to('bokeh_create.html')
def bokeh_form(request):
    form = BokehVisualForm()
    return {"user":request.user, 'form': form, "current":"bokeh"}
