from django.http import JsonResponse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User

from usuarios.models import TiposUsuarios, Empresas, Plataformas, EmpresasUsuarios


# Create your views here.

class LoginView(TemplateView):
    """docstring for LoginView"""
    template_name = 'administracion/login.html'


class DashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """docstring for DashboardView"""
    login_url = 'usuarios:login'
    template_name = 'administracion/dashboard.html'

    def test_func(self):
        return self.request.user.tiposusuarios.tipo == 'A'


class CreateUserView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    login_url = 'usuarios:login'
    template_name = 'administracion/nuevo_usuario.html'

    def test_func(self):
        return self.request.user.tiposusuarios.tipo == 'A'

    def post(self, request, *args, **kwargs):
        body = dict(request.POST)

        user = User.objects.filter(username=body['username'][0])

        if user:
            return JsonResponse({"error": "El nombre del usuario ya existe"})
        else:
            return JsonResponse({"ok": "El nombre esta disponible"})


class CrearClienteView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    login_url = 'usuarios:login'
    template_name = 'administracion/nuevo_cliente.html'

    def test_func(self):
        return self.request.user.tiposusuarios.tipo == 'A'
       