"""Logica para manejar los procesos de Soporte."""

import json

from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db import transaction
from django.http import JsonResponse
from django.views.generic import TemplateView, View

from usuarios.models import (
    Incidentes,
    UsuariosSoporteIncidentes,
    MovimientosIncidentes,
    EstadosIncidentes,
    Adjuntos
)


class HomeSoporteView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Home para los clientes de Grexco.

        :url    :soporte/
    """

    login_url = 'usuarios:login'
    template_name = 'soporte/home.html'

    def test_func(self):
        """
        Retringe el acceso de usuarios.

        Solo permite el acceso a los usuarios:
            - Administrador
            - Soporte
        """
        tipo = self.request.user.usuariosgrexco.tipo
        return tipo == 'A' or tipo == 'S'


class ListadoIncidentesView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Retorna un listado de todos los incidentes creados.

        :url :soporte/incidentes/listado/
    """

    login_url = 'usuarios:login'

    def test_func(self):
        """
        Retringe el acceso de usuarios.

        Solo permite el acceso a los usuarios:
            - Administrador
            - Soporte
        """
        tipo = self.request.user.usuariosgrexco.tipo
        return tipo == 'A' or tipo == 'S'

    def get(self, request):
        """docstring."""
        usuario = self.request.user
        coordinador = self.request.user.usuariosgrexco.es_coordinador

        if coordinador is True:
            qry_incidentes = (
                Incidentes.objects
                          .all()
                          .values(
                              'codigo',
                              'titulo',
                              'aplicacion__nombre',
                              'estado__descripcion',
                              'fecha_creacion',
                              'usuario__usuariosgrexco__empresa__nombre'
                          )
            )
            incidentes = []
            for incidente in qry_incidentes:
                incidente['fecha_creacion'] = datetime.strftime(
                    incidente['fecha_creacion'], format='%Y-%m-%d')
                incidentes.append(incidente)

            return JsonResponse({'incidentes': incidentes}, status=200)
        else:
            print('usuario no coordinador')
            qry_incidentes = (
                UsuariosSoporteIncidentes.objects
                                         .filter(usuario=usuario,
                                                 incidente__estado='S')
                                         .values(
                                             'incidente__codigo',
                                             'incidente__titulo',
                                             'incidente__aplicacion__nombre',
                                             'incidente__estado__descripcion',
                                             'incidente__fecha_creacion',
                                             'usuario__usuariosgrexco__empresa__nombre'
                                         )
            )
            incidentes = []
            for incidente in qry_incidentes:
                incidentes.append(incidente)
            return JsonResponse({'incidentes': incidentes}, status=200)


class DetalleIncidentesView(
        LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """Template para consulta un incidente."""

    login_url = 'usuarios:login'
    template_name = 'soporte/detalle_incidente.html'

    def test_func(self):
        """
        Retringe el acceso de usuarios.

        Solo permite el acceso a los usuarios:
            - Administrador
            - Soporte
        """
        tipo = self.request.user.usuariosgrexco.tipo
        return tipo == 'A' or tipo == 'S'

    def get_context_data(self, *args, **kwargs):
        """Envia la información del Incidente consultado."""
        codigo = kwargs['codigo']
        incidente = Incidentes.objects.get(codigo=codigo)

        adjuntos = Adjuntos.objects.filter(incidente=incidente)
        return {'codigo': codigo, 'incidente': incidente, 'adjuntos': adjuntos}


class ConsultaUsuariosSoporteView(
        LoginRequiredMixin, UserPassesTestMixin, View):
    """Retorna un listado Json con los nombres de usuario de los empleados
    de soporte ACTIVOS.
    """

    login_url = 'usuarios:login'

    def test_func(self):
        """
        Retringe el acceso de usuarios.

        Solo permite el acceso a los usuarios:
            - Administrador
            - Soporte
            - Tecnologia
        """
        tipo = self.request.user.usuariosgrexco.tipo
        return tipo == 'A' or tipo == 'S' or tipo == 'T'

    def get(self, request):
        usuarios = list(User.objects.filter(
            is_active=True, usuariosgrexco__tipo='S').values('username'))
        return JsonResponse({'usuarios': usuarios}, status=200)


class AsignaIncidentesSoporteView(
        LoginRequiredMixin, UserPassesTestMixin, View):
    """Vista para asignar incidentes a los empleados de Soporte."""

    login_url = 'usuarios:login'

    def test_func(self):
        """
        Restringe el acceso de usuarios.

        Solo permite el acceso a los usuarios:
            - Administrador
            - Soporte
            - Tecnologia
        """
        tipo = self.request.user.usuariosgrexco.tipo
        es_coordinador = self.request.user.usuariosgrexco.es_coordinador

        if tipo == 'A':
            return True
        elif tipo == 'S' and es_coordinador is True:
            return True
        else:
            return False

    def get(self, request):
        return JsonResponse({'ok': 'ok'}, status=200)

    def post(self, request, *args, **kwargs):
        """Recibe el codigo del usuario y de incidente para asignar el
        incidente al usuario."""
        data = json.loads(request.body.decode('utf-8'))
        cod_usuario = data['usuario']
        cod_incidente = data['incidente']
        cod_prioridad = data['prioridad']
        print(cod_prioridad, cod_incidente, cod_usuario)
        estado = EstadosIncidentes.objects.get(codigo='S')

        with transaction.atomic():
            # Verifica que el incidente no tenga usuario se Soporte asignado.
            qry_usuario_soporte = UsuariosSoporteIncidentes.objects.filter(
                incidente=cod_incidente)
            if qry_usuario_soporte:
                return JsonResponse(
                    {'error': 'El incidente ya tiene un usuario asignado'},
                    status=400)

            # Asigna el Usuario al Incidente.
            usr_soporte = User.objects.get(username=cod_usuario)
            incidente = Incidentes.objects.get(codigo=cod_incidente)
            u = UsuariosSoporteIncidentes(
                usuario=usr_soporte, incidente=incidente)
            try:
                u.save()
            except Exception as e:
                return JsonResponse({'error': e}, status=400)

            # Cambia el estado del Incidente.
            incidente.estado = estado
            try:
                incidente.save()
            except Exception as e:
                return JsonResponse({'error': e}, status=400)

            # Guarda los movimientos del Incidente.
            usr_coordinador = self.request.user
            movimiento = MovimientosIncidentes(
                incidente=incidente,
                estado=estado,
                responsable=usr_coordinador)
            try:
                movimiento.save()
            except Exception as e:
                return JsonResponse({'error': e}, status=400)

            # Si NO hay ningún error.
            return JsonResponse(
                {'ok': 'Se asignó el incidente correctamente'}, status=200)
