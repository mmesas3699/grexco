"""Vistas para la aplicación Usuarios."""
from datetime import datetime

from django.contrib.auth import authenticate, login  # , logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, HttpResponse
from django.views.generic import TemplateView
from django.views.generic import View

from administracion.models import Aplicaciones, UsuariosGrexco
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


def convert_datetime_to_string(o):
    """docstring."""
    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M:%S"

    if isinstance(o, datetime.date):
        return o.strftime(DATE_FORMAT)
    elif isinstance(o, datetime.time):
        return o.strftime(TIME_FORMAT)
    elif isinstance(o, datetime.datetime):
        return o.strftime("%s %s" % (DATE_FORMAT, TIME_FORMAT))


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
    """Template para consultar incidentes del cliente que este loggeado."""

    login_url = 'usuarios:login'
    template_name = 'usuarios/incidentes.html'

    def test_func(self):
        """
        Retringe el acceso de usuarios.

        Solo permite el acceso a los usuarios:
            - Administrador
            - Cliente
        """
        tipo = self.request.user.usuariosgrexco.tipo
        return tipo == 'A' or tipo == 'C'


class CodigoIncidentesJsonView(LoginRequiredMixin, UserPassesTestMixin, View):
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

    def post(self, request, *args, **kwargs):
        """Guardar los incidentes y sus archivos adjuntos."""
        data = dict(request.POST)
        codigo = data['codigo'][0]
        descripcion = data['descripcion'][0]
        aplicacion_id = data['selAplicacion'][0]
        titulo = data['titulo'][0]
        usuario = self.request.user.usuariosgrexco
        aplicacion = get_object_or_404(Aplicaciones, id=aplicacion_id)
        estado = get_object_or_404(EstadosIncidentes, codigo='C')

        with transaction.atomic():
            # Guarda el incidente
            incidente = Incidentes(
                codigo=codigo,
                descripcion=descripcion,
                titulo=titulo,
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


class IncidentesConsultaIndividualJsonView(
        LoginRequiredMixin, UserPassesTestMixin, View):
    """Retorna un JSON con la info del Incidente consultado."""

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

    def get(self, request, **kwargs):
        """Retorna un Json con la información del incidente consultado."""
        codigo = kwargs['codigo']
        qry_incidente = Incidentes.objects.filter(codigo=codigo).values()
        qry_adjuntos = Adjuntos.objects.filter(
            incidente__codigo=codigo).values('archivo')

        if qry_incidente:
            incidente = qry_incidente[0]
            listado_adjuntos = []
            for archivo in qry_adjuntos:
                for k, v in archivo.items():
                    listado_adjuntos.append(v)

            return JsonResponse(
                {'incidente': incidente, 'adjuntos': listado_adjuntos},
                status=200
            )
        else:
            return JsonResponse(
                {'incidente': 'No hay incidentes con este código'},
                status=400
            )


class IncidentesConsultaView(
        LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Template para consultar un incidente.

    url =
    """

    login_url = 'usuarios:login'
    template_name = 'usuarios/incidentes_consulta.html'

    def test_func(self):
        """
        Retringe el acceso de usuarios.

        Solo permite el acceso a los usuarios:
            - Administrador
            - Cliente
        """
        tipo = self.request.user.usuariosgrexco.tipo
        return tipo == 'A' or tipo == 'C'


class IncidentesConsultaUsuarioJsonView(
        LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Retorna un listado de incidentes creados por el usuario loggeado.

    url = 'incidentes/consulta/por-usuario/'
    """

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
        """Retorna un JSON con los incidentes creados por el Usuario."""
        usuario_grexco = UsuariosGrexco.objects.get(usuario=self.request.user)
        qry_incidentes = (
            Incidentes.objects
                      .filter(usuario=usuario_grexco)
                      .values(
                          'codigo',
                          'titulo',
                          'aplicacion__nombre',
                          'estado__descripcion',
                          'fecha_creacion'
                      )
        )

        incidentes = []
        for incidente in qry_incidentes:
            incidente['fecha_creacion'] = datetime.strftime(
                incidente['fecha_creacion'], format='%Y-%m-%d')
            incidentes.append(incidente)

        return JsonResponse({'incidentes': incidentes}, status=200)
