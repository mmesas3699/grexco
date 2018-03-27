from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from administracion.views import DashboardView


# Create your views here.


class LoginView(TemplateView):
    """docstring for LoginView"""
    template_name = 'usuarios/login.html'

    def post(self, request):
        usrname = request.POST['name']
        # print(usrname)
        pwd = request.POST['pwd']
        # print(pwd)
        user = authenticate(request, username=usrname, password=pwd)
        # print(user)
        
        if user is not None:
            login(request, user)
            return redirect('administracion:dashboard')
        else:
            return HttpResponse('Datos invalidos o usuario inactivo')

