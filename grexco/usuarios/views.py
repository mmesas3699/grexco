from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.views.generic import TemplateView

# Create your views here.


class LoginView(TemplateView):
    """docstring for LoginView"""
    template_name = 'usuarios/login.html'
