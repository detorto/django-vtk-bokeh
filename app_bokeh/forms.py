#coding: utf-8
from django import forms
import app_bokeh.models as models

class BokehVisualForm(forms.Form):
    title = forms.CharField(max_length=200, label=u"Title")
    description = forms.CharField(widget=forms.Textarea, label=u"Description")
    width = forms.IntegerField(label=u"Width")
    height = forms.IntegerField(label=u"Height")
    use_wgl = forms.BooleanField(label="Use wgl", required=False)
    img_type =  forms.ChoiceField(choices=models.img_type_choices, label=u"Image type")
    inputfile = forms.FileField(label=u"Visualization file")
