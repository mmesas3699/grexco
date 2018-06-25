"""Vistas para la aplicación Usuarios."""

from django.contrib.auth import authenticate, login  # , logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from django.views.generic import TemplateView
from django.views.generic import View

# from administracion.views import genera_id, empresa_activa


class LoginView(TemplateView):
    """docstring for LoginView."""

    template_name = 'usuarios/login.html'

    def post(self, request):
        """docstring."""
        data = dict(request.POST)
        usuario = data['usuario'][0]
        password = data['contraseña'][0]
        user = authenticate(request, username=usuario, password=password)

        if user is not None:
            login(request, user)

            # Dependiendo del tipo de usuario se envia una URL
            # para redireccionar
            tipo = user.usuariosgrexco.tipo
            if tipo == 'A':
                return JsonResponse({'url': '/a/'}, status=200)
            elif tipo == 'C':
                return JsonResponse({'url': '/usuarios/'}, status=200)
            else:
                return JsonResponse({'url': '/'}, status=200)
        else:
            return HttpResponse('Datos invalidos o usuario inactivo')


class HomeUsuariosView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """Home para los clientes de Grexco."""

    login_url = 'usuarios:login'
    template_name = 'usuarios/index_usuarios.html'

    def test_func(self):
        """
        Retringe el acceso de usuarios.

        Solo permite el acceso a los usuarios:
            - Administrador
            - Cliente
        """
        tipo = self.request.user.usuariosgrexco.tipo
        return tipo == 'A' or tipo == 'C'


class IncidentesView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """Template para consultar incidentes del cliente que loggeado."""

    login_url = 'usuarios:login'
    template_name = 'usuarios/base_contenido.html'

    def test_func(self):
        """
        Retringe el acceso de usuarios.

        Solo permite el acceso a los usuarios:
            - Administrador
            - Cliente
        """
        tipo = self.request.user.usuariosgrexco.tipo
        return tipo == 'A' or tipo == 'C'
