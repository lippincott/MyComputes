from django.views.generic import TemplateView
from django.views import generic
from django.http import HttpResponseRedirect, Http404


from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect



### Home Page
class HomePage(generic.TemplateView):
    template_name = 'index.html'

    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.is_authenticated:
    #         return redirect(reverse('dashboard:dashboard'))  # replace
    #     return super().dispatch(request, *args, **kwargs)
