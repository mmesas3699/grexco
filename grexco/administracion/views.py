# from django.shortcuts import render
# from django.shortcuts import HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.


class LoginView(TemplateView):
    """docstring for LoginView"""
    template_name = 'administracion/login.html'


class DashboardView(LoginRequiredMixin, TemplateView):
    """docstring for DashboardView"""
    login_url = 'usuarios:login'
    template_name = 'administracion/dashboard.html'


class CreateUserView(TemplateView):
    template_name = 'administracion/nuevo_usuario.html'
