"""Vistas para la aplicación Usuarios."""
# import json

from django.contrib.auth import authenticate, login  # , logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, HttpResponse
from django.views.generic import TemplateView
from django.views.generic import View

from administracion.models import Aplicaciones
# from administracion.views import genera_id, empresa_activa

from usuarios.models import Adjuntos
from usuarios.models import EstadosIncidentes
from usuarios.models import Incidentes
from usuarios.models import MovimientosIncidentes


def codigos_incidentes():
    """Genera los codigo de los incidentes."""
    ultimo_incidente = Incidentes.objects.last()

    if ultimo_incidente is None:
        codigo = 1
    else:
        codigo = ultimo_incidente.codigo + 1

    return codigo


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

            # Dependiendo del tipo de usuario se envia a una URL
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
    template_name = 'usuarios/home_usuarios.html'

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


class CodigoIncidentesView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Vista para generar los codigos de los incidentes."""

    login_url = 'usuarios:login'

    def test_func(self):
        """
        Retringe el acceso de usuarios.

        Solo permite el acceso a los usuarios:
            - Administrador
            - Cliente
        """
        tipo = self.request.user.usuariosgrexco.tipo
        return tipo == 'A' or tipo == 'C'

    def get(self, request):
        """Retorna un JSON con el código del incidente."""
        codigo = codigos_incidentes()
        return JsonResponse({'codigo': codigo}, status=200)


class IncientesNuevoView(
        LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """Template para capturar un nuevo incidente."""

    login_url = 'usuarios:login'
    template_name = 'usuarios/incidentes_nuevo.html'

    def test_func(self):
        """
        Retringe el acceso de usuarios.

        Solo permite el acceso a los usuarios:
            - Administrador
            - Cliente
        """
        tipo = self.request.user.usuariosgrexco.tipo
        return tipo == 'A' or tipo == 'C'


class GuardaIncidentesView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Guarda los incidentes y sus archivos adjuntos."""

    login_url = 'usuarios:login'

    def test_func(self):
        """
        Retringe el acceso de usuarios.

        Solo permite el acceso a los usuarios:
            - Administrador
            - Cliente
        """
        tipo = self.request.user.usuariosgrexco.tipo
        return tipo == 'A' or tipo == 'C'

    def post(self, request, *args, **kwargs):
        """Guardar los incidentes y sus archivos adjuntos."""
        data = dict(request.POST)
        codigo = data['codigo'][0]
        descripcion = data['descripcion'][0]
        aplicacion_id = data['selAplicacion'][0]
        usuario = self.request.user.usuariosgrexco
        aplicacion = get_object_or_404(Aplicaciones, id=aplicacion_id)
        estado = get_object_or_404(EstadosIncidentes, codigo='C')

        with transaction.atomic():
            # Guarda el incidente
            incidente = Incidentes(
                codigo=codigo,
                descripcion=descripcion,
                usuario=usuario,
                aplicacion=aplicacion,
                estado=estado
            )
            try:
                incidente.save()
            except Exception as e:
                return JsonResponse(
                    {'error': 'Ocurrio un error: {}'.format(e)}, status=400)

            # Guarda los archivos adjuntos
            if request.FILES:
                archivos = request.FILES.getlist('inpAdjuntos')
                for archivo in archivos:
                    adjunto = Adjuntos(incidente=incidente, archivo=archivo)
                    try:
                        adjunto.save()
                    except Exception as e:
                        return JsonResponse(
                            {'error': 'Ocurrio un error: {}'.format(e)},
                            status=400
                        )
                        break
            else:
                print('No hay adjuntos')

            # Guarda el movimiento
            movimiento = MovimientosIncidentes(
                incidente=incidente, estado=estado, responsable=usuario)
            try:
                movimiento.save()
            except Exception as e:
                return JsonResponse(
                    {'error': 'Ocurrio un error: {}'.format(e)}, status=400)

            return JsonResponse({'ok': 'Se creó el incidente correctamente'})
