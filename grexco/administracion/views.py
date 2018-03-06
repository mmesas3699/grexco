# from django.shortcuts import render
# from django.shortcuts import HttpResponse
from django.views.generic import TemplateView


# Create your views here.


class LoginView(TemplateView):
    """docstring for LoginView"""
    template_name = 'administracion/login.html'


class DashboardView(TemplateView):
    """docstring for DashboardView"""
    template_name = 'administracion/dashboard.html'


class NewUserView(TemplateView):
    template_name = 'administracion/nuevo_usuario.html'
