from django import forms
from django.forms import widgets
from . import models

# Generic Post Form
class ReportForm(forms.ModelForm):
# class PostForm(LoginRequiredMixin, forms.ModelForm):

    class Meta:
        exclude = ('created_at', 'slug', 'last_modified','slug',)
        model = models.Report


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for visible in self.fields.values():
            if (isinstance(visible.widget, widgets.Select)):
                visible.widget.attrs['class'] = 'form-control form-select'
            elif (isinstance(visible.widget, widgets.CheckboxInput)):
                visible.widget.attrs['class'] = 'form-check-input'
            else:
                visible.widget.attrs['class'] = 'form-control'
            visible.widget.attrs['data-lpignore'] = "true"
            visible.widget.attrs['autocomplete'] = "off"




class ReportUpdateForm(forms.ModelForm):

    class Meta:
        exclude = ('created_at', 'slug', 'last_modified','slug',)
        model = models.Report

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for visible in self.fields.values():
            if (isinstance(visible.widget, widgets.Select)):
                visible.widget.attrs['class'] = 'form-control form-select'
            elif (isinstance(visible.widget, widgets.CheckboxInput)):
                visible.widget.attrs['class'] = 'form-check-input'
            else:
                visible.widget.attrs['class'] = 'form-control'
            visible.widget.attrs['data-lpignore'] = "true"
            visible.widget.attrs['autocomplete'] = "off"
