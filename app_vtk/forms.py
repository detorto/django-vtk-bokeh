from django import forms
import app_vtk.models as models

class VtkjsVisualForm(forms.Form):
    title = forms.CharField(max_length=200, label=u"Title")
    description = forms.CharField(widget=forms.Textarea, label=u"Description")
    width = forms.IntegerField(label=u"Width")
    height = forms.IntegerField(label=u"Height")
    inputfile = forms.FileField(label=u"Visualization file")
