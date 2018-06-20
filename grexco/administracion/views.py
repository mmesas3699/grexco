"""docstring."""
import json
from datetime import time

import pyexcel as pe
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django.db import IntegrityError
from django.db import transaction
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.views.generic import View

from administracion.models import Aplicaciones
from administracion.models import Convenios
from administracion.models import Empresas
from administracion.models import HorariosSoporte
from administracion.models import Plataformas
from administracion.models import PrioridadesRespuesta
from administracion.models import Reportes
from administracion.models import TiemposRespuesta
from administracion.models import UsuariosGrexco


def genera_id(modelo):
    """Recibe como parametro un Modelo de: administracion.models."""
    x = modelo.objects.last()
    if x is None:
        return 1
    else:
        return x.id + 1


def empresa_activa(nit):
    """
    Retorna True si la empresa esta activa, si no retorna False.

    Recibe como parametro el nit de la empresa a consultar.

    """
    empresa = get_object_or_404(Empresas, nit=nit)

    if empresa.activa:
        return True
    else:
        return False


def sql_a_diccionario(cursor):
    """Retorna las filas de la consulta como un diccionario."""
    columnas = [columna[0] for columna in cursor.description]
    return [dict(zip(columnas, fila)) for fila in cursor.fetchall()]


class LoginView(TemplateView):
    """docstring for LoginView."""

    template_name = 'administracion/login.html'

    def post(self, request):
        """m."""
        data = dict(request.POST)
        usuario = authenticate(
            request, username=data['nombre'][0],
            password=data['contraseña'][0])

        if usuario is not None:
            login(request, usuario)
            return JsonResponse({'ok': 'ok'}, status=200)
        else:
            return JsonResponse(
                {"error": "Datos invalidos o usuario inactivo"}, status=400)


# ............................................................................
# .                             Dahsboard                                    .
# ............................................................................
class DashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """docstring for DashboardView."""

    login_url = 'usuarios:login'
    template_name = 'administracion/dashboard.html'

    def test_func(self):
        """docstring."""
        return self.request.user.usuariosgrexco.tipo == 'A'


# ****************************************************************************
# *                            Plataformas                                   *
# ****************************************************************************

class PlataformasView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """Vista para consultar plataformas."""

    login_url = 'administracion:admin_login'
    template_name = 'administracion/plataformas.html'

    def test_func(self):
        """Restringe el acceso solo a usuario administrador."""
        return self.request.user.usuariosgrexco.tipo == 'A'

    def get_context_data(self, *args, **kwargs):
        """Retorna un listado de las plataformas creadas."""
        plataforma = Plataformas.objects.all()

        return {'plataformas': plataforma}


class CrearPlataformasView(
        LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Vista para crear plataformas.

    * url: plataformas/nuevo/
    """

    login_url = 'usuarios:login'
    template_name = 'administracion/nueva_plataforma.html'

    def test_func(self):
        """Restringe el acceso solo a usuario administrador."""
        return self.request.user.usuariosgrexco.tipo == 'A'

    def post(self, request, *args, **kwargs):
        """Recibe los datos enviados para crear la nueva plataforma."""
        data = dict(request.POST)
        nombre = data['nombre'][0]
        version = data['version'][0]

        if not nombre or not version:
            return JsonResponse(
                {"error": "Los campos están vacíos"}, status=400)

        plataforma = Plataformas.objects.filter(
            nombre=nombre.upper(), version=version.upper())

        # Verifica si la plataforma ya existe
        if plataforma.exists():

            # Si existe retorna un error
            return JsonResponse({"error": "Los datos ya existen"}, status=400)
        else:

            # Si No existe la crea
            id = genera_id(Plataformas)
            plt = Plataformas(id=id, nombre=nombre.upper(), version=version)

            with transaction.atomic():
                try:
                    plt.save()
                except Exception as e:
                    mensaje = """
                            Ocurrió un error al grabar los datos: {}
                        """.format(e)
                    return JsonResponse({"error": mensaje}, status=400)

                mensaje = "Se guardó la plataforma: {}".format(plt)
                return JsonResponse({"ok": mensaje})


class EliminarPlataformasView(
        LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """Vista para eliminar una plataforma."""

    login_url = 'usuarios:login'
    template_name = 'administracion/companies.html'

    def test_func(self):
        """Restringe el acceso solo a usuario administrador."""
        return self.request.user.usuariosgrexco.tipo == 'A'

    def post(self, request, *args, **kargs):
        """docstring."""
        data = dict(request.POST)
        # print(data)
        with transaction.atomic():
            for k, v in data.items():
                plataforma = get_object_or_404(Plataformas, id=int(data[k][0]))
                if plataforma:
                    from django.db.models.deletion import ProtectedError
                    try:
                        plataforma.delete()
                    except ProtectedError:
                        empresa = Empresas.objects.get(
                            plataforma__id=plataforma.id)
                        msj = """
                                No es posible eliminar: {}-{}.
                                Pertenece a la empresa: {}
                               """.format(
                            plataforma.nombre,
                            plataforma.version,
                            empresa.nombre
                        )
                        return JsonResponse({"error": msj}, status=400)

        mensaje = 'Se eliminó la plataforma: {}'.format(plataforma.nombre)
        return JsonResponse({"ok": mensaje}, status=200)


class ListadoBasicoPlataformasView(
        LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Retorna un Json con los datos de las plataformas.

    Con el formato:
    """

    login_url = 'usuarios:login'

    def test_func(self):
        """Restringe el acceso solo a usuario administrador."""
        return self.request.user.usuariosgrexco.tipo == 'A'

    def get(self, request, *args, **kwargs):
        """docstring."""
        qry_plataformas = Plataformas.objects.values().all()
        plataformas = []
        for plataforma in qry_plataformas:
            plataformas.append(plataforma)

        return JsonResponse({'plataformas': plataformas}, status=200)


# ............................................................................
# .                                Aplicaciones                              .
# ............................................................................
class AplicationsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """Vista para consultar las aplicaciones."""

    login_url = 'usuarios:login'
    template_name = 'administracion/aplicaciones.html'

    def test_func(self):
        """Restringe el acceso solo a usuario administrador."""
        return self.request.user.usuariosgrexco.tipo == 'A'

    def get_context_data(self, *args, **kwargs):
        """docstring."""
        aplicaciones = Aplicaciones.objects.all()
        return {'aplicaciones': aplicaciones}

    def post(self, request, *args, **kwargs):
        """Retorna la información de: Versión y Convenios."""
        data = dict(request.POST)
        id = data['id'][0]
        app = Aplicaciones.objects.get(id=id)

        convenios = []
        qry_convenios = app.convenios.values(
            'empresa__nombre', 'empresa__nit').all()
        if len(qry_convenios) == 0:
            dic_convenios = {
                'empresa': 'Esta aplicación no es usada por ningún Cliente.'
            }
            convenios.append(dic_convenios)
        else:
            for convenio in qry_convenios:
                dic_convenios = {}
                dic_convenios['empresa'] = convenio['empresa__nombre']
                dic_convenios['nit'] = convenio['empresa__nit']
                convenios.append(dic_convenios)

        versiones = []
        qry_versiones = (
            app.versiones
               .values('version', 'fecha')
               .all()
               .order_by('-version')
        )
        if len(qry_versiones) == 0:
            dic_versiones = {
                'version': 'No tiene versiones',
                'fecha': 'No tiene versiones'
            }
            versiones.append(dic_versiones)
        else:
            for ver in qry_versiones:
                dic_versiones = {}
                dic_versiones['version'] = ver['version']
                dic_versiones['fecha'] = ver['fecha'].strftime(
                    format='%Y-%m-%d')
                versiones.append(dic_versiones)

        aplicacion = {
            'aplicacion': app.nombre,
            'versiones': versiones,
            'convenios': convenios
        }
        return JsonResponse({'aplicacion': aplicacion}, status=200)


class CreateAplicationsView(
        LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """Vista para crear Aplicaciones."""

    login_url = 'usuarios:login'

    def test_func(self):
        """Restringe el acceso solo a usuario administrador."""
        return self.request.user.usuariosgrexco.tipo == 'A'

    def post(self, request, *args, **kwargs):
        """Si POST trae datos se crea la aplicacion por formulario."""
        data = request.POST
        if len(data) == 1:
            id = genera_id(Aplicaciones)
            nombre = data['nombre']
            app = Aplicaciones(id=id, nombre=nombre)
            if Aplicaciones.objects.filter(nombre=nombre).exists():
                return JsonResponse(
                    {'error': 'La aplicación: {}. Ya existe.'.format(nombre)},
                    status=400
                )

            try:
                app.save()
            except Exception as e:
                return JsonResponse(
                    {'error': 'Ocurrio un error {}'.format(e)},
                    status=400
                )

            return JsonResponse(
                {'ok': 'Se creo la aplicación: {}'.format(nombre)},
                status=200
            )
        else:
            file = request.FILES['archivo']
            file_type = file.name.split('.')[-1]
            cuenta_guardados = 0
            no_grabados = []
            data = pe.iget_records(file_stream=file, file_type=file_type)
            n_columnas = pe.get_sheet(
                file_stream=file, file_type=file_type).number_of_rows() - 1
            for row in data:
                id = genera_id(Aplicaciones)
                nombre = row['Aplicaciones']
                if Aplicaciones.objects.filter(nombre=nombre).exists():
                    msj = {'err': 'Ya existe', 'app': nombre}
                    no_grabados.append(msj)
                else:
                    app = Aplicaciones(id=id, nombre=nombre)
                    try:
                        app.save()
                    except Exception as e:
                        return JsonResponse(
                            {'error': 'Ocurrio un error: {}'.format(e)},
                            status=400
                        )

                    cuenta_guardados = cuenta_guardados + 1

            if cuenta_guardados == n_columnas:
                return JsonResponse(
                    {'ok': 'Se grabaron todas las Aplicaciones'},
                    status=200
                )
            else:
                respuesta = "Se grabaron {} de {}".format(
                    cuenta_guardados, n_columnas)
                return JsonResponse(
                    {
                        'error': {
                            'respuesta': respuesta,
                            'aplicaciones': no_grabados
                        }
                    },
                    safe=False,
                    status=400
                )


class DeleteAplicationsView(
        LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Vista para eliminar Aplicaciones.

    Solo si la aplicación no tiene versiones, convenios o reportes.
    """

    login_url = 'usuarios:login'

    def test_func(self):
        """Restringe el acceso solo a usuario administrador."""
        return self.request.user.usuariosgrexco.tipo == 'A'

    def post(self, request, *args, **kwargs):
        """docstring."""
        data = dict(request.POST)
        id = data["aplicacion[0][]"][0]

        try:
            app = Aplicaciones.objects.get(id=id)
        except ObjectDoesNotExist:
            return JsonResponse(
                {'error': 'La aplicacion no existe'}, status=400)

        convenios = app.convenios.all()
        versiones = app.versiones.all()
        reportes = app.reportes.all()

        if len(convenios) > 0 or len(versiones) > 0 or len(reportes) > 0:
            return JsonResponse(
                {
                    'error':
                        """No es posible eliminar {}.
                        Está siendo usada""".format(app.nombre)
                },
                status=400
            )
        else:
            app.delete()
            return JsonResponse(
                {'ok': 'Se eliminó la aplicación: {}'.format(app.nombre)},
                status=200)


class ListadoAplicacionesView(
        LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Retorna un JSON con la información (id y nombre) de la aplicación.

    url = aplicaciones/listado/

    """

    login_url = 'usuarios:login'

    def test_func(self):
        """Restringe el acceso solo a usuario administrador."""
        return self.request.user.usuariosgrexco.tipo == 'A'

    def get(self, request, *args, **kwargs):
        """docstring."""
        qry_aplicaciones = (
            Aplicaciones.objects
                        .values('id', 'nombre')
                        .all()
                        .order_by('id')
        )
        aplicaciones = []
        for aplicacion in qry_aplicaciones:
            aplicaciones.append(aplicacion)

        return JsonResponse({'aplicaciones': aplicaciones}, status=200)


class ListExcelAplicationsView(
        LoginRequiredMixin, UserPassesTestMixin, View):
    """Retorna un archivo de excel con el listado de las aplicaciones."""

    login_url = 'usuarios:login'

    def test_func(self):
        """Restringe el acceso solo a usuario administrador."""
        return self.request.user.usuariosgrexco.tipo == 'A'

    def get(self, request, *args, **kwargs):
        """docstring."""
        qry_aplicaciones = Aplicaciones.objects.values(
            'id', 'nombre').order_by('id')
        aplicaciones = []
        for aplicacion in qry_aplicaciones:
            aplicaciones.append(aplicacion)

        excel = pe.get_sheet(records=aplicaciones)
        excel.save_as(filename='/tmp/aplicaciones.xlsx')
        with open('/tmp/aplicaciones.xlsx', 'rb') as excel:
            response = HttpResponse(excel.read())
            response['content_type'] = 'application/vnd.ms-excel'
            response['Content-Disposition'] = 'attachment; filename="/tmp/aplicaciones.xlsx"'
            return response


# ****************************************************************************
# *                                  REPORTES                                *
# ****************************************************************************
class ReportsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """Vista reportes."""

    login_url = 'usuarios:login'
    template_name = 'administracion/reportes.html'

    def test_func(self):
        """Restringe el acceso solo a usuario administrador."""
        return self.request.user.usuariosgrexco.tipo == 'A'

    def post(self, request, *args, **kwargs):
        """docstring."""
        qry_reportes = (
            Reportes.objects
                    .values('id', 'nombre', 'aplicacion__nombre')
                    .all()
        )
        reportes = []
        for reporte in qry_reportes:
            reportes.append(reporte)

        return JsonResponse(reportes, safe=False)


class CreateReportsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Vista para crear reportes.

    La vista recibe un JSON con los datos:
        - tipo (si la aplicación se crea de forma invidual o
                masivamente por archivo de excel)
        - nombre (del reporte)
        - aplicacion (el id de la aplicación a la que pertenece el reporte)
    """
    login_url = 'usuarios:login'

    def test_func(self):
        """Restringe el acceso solo a usuario administrador."""
        return self.request.user.usuariosgrexco.tipo == 'A'

    def post(self, request, *args, **kwargs):
        """docstring."""
        data = dict(request.POST)
        tipo = data['tipo'][0]

        # Si el tipo es individual
        if tipo == 'individual':

            # Id aplicación
            id_app = data['aplicacion'][0]
            nombre_reporte = data['nombre'][0].strip()

            # Verifica que los datos no esten vacios
            if not id_app:
                return JsonResponse(
                    {"error": "Debe seleccionar la aplicación a la que pertenece el reporte"},
                    status=400
                )
            elif not nombre_reporte:
                return JsonResponse(
                    {"error": "El nombre del reporte es obligatorio"},
                    status=400
                )

            # Calcula el Id del reporte
            id_reporte = genera_id(Reportes)

            # Consulta la aplicación
            app = Aplicaciones.objects.get(id=id_app)

            # Crea el objeto reporte
            reporte = Reportes(
                id=id_reporte, nombre=nombre_reporte, aplicacion=app)
            try:
                reporte.save()
            except IntegrityError:
                return JsonResponse(
                    {
                        "error": "¡El reporte '{}' ya existe!".format(
                            reporte.nombre)
                    },
                    status=400
                )

            return JsonResponse(
                {"ok": "Se creó el reporte: '{}'".format(reporte.nombre)},
                status=200)
        elif tipo == 'excel':
            archivo = request.FILES['archivo']
            tipo_archivo = archivo.name.split('.')[-1]

            # Transforma el archivo de Excel en una Lista de Python
            # el archivo debe tener dos columnas de datos por cada fila
            # y ordenado así:
            #               0               1
            #      | Nombre reporte | Id aplicación |
            excel = pe.get_array(
                file_stream=archivo, file_type=tipo_archivo, start_row=1)
            cuenta_grabados = 0
            no_grabados = []
            n_columnas = len(excel)
            for fila in excel:
                nombre_reporte = fila[0]
                if Reportes.objects.filter(nombre=nombre_reporte).exists():
                    msj = {'err': 'Ya existe', 'reporte': nombre_reporte}
                    no_grabados.append(msj)
                else:
                    id_reporte = genera_id(Reportes)
                    aplicacion = Aplicaciones.objects.get(id=fila[1])
                    reporte = Reportes(
                        id=id_reporte, nombre=nombre_reporte,
                        aplicacion=aplicacion)
                    try:
                        reporte.save()
                    except Exception as e:
                        return JsonResponse(
                            {'error': 'Ocurrio un error: {}'.format(e)},
                            status=400)

                    cuenta_grabados = cuenta_grabados + 1

            if cuenta_grabados == n_columnas:
                return JsonResponse(
                    {'ok': 'Se grabaron todos los reportes'}, status=200,
                    safe=False)
            else:
                respuesta = "Se grabaron {} de {}".format(
                    cuenta_grabados, n_columnas)
                return JsonResponse(
                    {'error':
                        {'respuesta': respuesta, 'reportes': no_grabados}},
                    safe=False,
                    status=400
                )


class DetailReportView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Vista para consultar el detalle de un Reporte.
    """
    login_url = 'usuarios:login'
    template_name = 'administracion/reportes_detalle.html'

    def test_func(self):
        return self.request.user.usuariosgrexco.tipo == 'A'

    def get_context_data(self, **kwargs):
        id_reporte = kwargs['id']
        reporte = get_object_or_404(Reportes, id=id_reporte)
        qry_versiones = (
            reporte.versiones
                   .values('version', 'fecha')
                   .all()
                   .order_by('-fecha')
        )
        qry_incidentes = reporte.incidentes.values('codigo')
        info_reporte = {
            'reporte': reporte.nombre,
            'id': reporte.id,
            'aplicacion': reporte.aplicacion.nombre,
            'versiones': dict(qry_versiones),
            'incidentes': dict(qry_incidentes)
        }

        return {'reporte': info_reporte}


class UpdateReportsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Vista para editar el nombre de un Reporte.

    Recibe un JSON:
        {'id': [id], 'nuevo_nombre': [nuevo_nombre]}
    """
    login_url = 'usuarios:login'

    def test_func(self):
        return self.request.user.usuariosgrexco.tipo == 'A'

    def post(self, request, *args, **kwargs):
        data = dict(request.POST)
        id_reporte = data['id'][0]
        nuevo_nombre = data['nuevo_nombre'][0]

        if not Reportes.objects.filter(nombre=nuevo_nombre):
            if Reportes.objects.filter(id=id_reporte):
                reporte = Reportes.objects.get(id=id_reporte)
                nombre_antiguo = reporte.nombre

                # Cambia el nombre del reporte
                reporte.nombre = nuevo_nombre
                reporte.save()
                mensaje = 'El nuevo nombre del reporte "{}" es: {}'.format(
                    nombre_antiguo, nuevo_nombre)
                return JsonResponse({'ok': mensaje}, status=200)
            else:
                return JsonResponse(
                    {'error': 'No existe el reporte: {}'.format(nombre_antiguo)},
                    status=400
                )
        else:
            return JsonResponse(
                {'error': 'Ya existe un reporte con el mismo nombre'},
                status=400
            )


class DeleteReportsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Vista para Eliminar un reporte
    Recibe por POST un objetoJSON:
        {'reporte': [id_reporte]}
    """
    login_url = 'usuarios:login'

    def test_func(self):
        return self.request.user.usuariosgrexco.tipo == 'A'

    def post(self, request, *args, **kwargs):
        data = dict(request.POST)
        id_reporte = data['reporte'][0]

        if Reportes.objects.filter(id=id_reporte):
            reporte = Reportes.objects.get(id=id_reporte)
            try:
                reporte.delete()
            except Exception as e:
                return JsonResponse({'error': e}, status=400)

            mensaje_ok = 'Se eliminó el Reporte: {}'.format(reporte.nombre)
            return JsonResponse({'ok': mensaje_ok}, status=200)
        else:
            return JsonResponse(
                {'error': '¡El reporte No existe!'}, status=400)


# ............................................................................
# .                        Horarios de soporte                               .
# ............................................................................
class HorariosSoporteView(
        LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Vista para consultar los horarios de soporte por Empresa.
    """
    login_url = 'usuarios:login'
    template_name = 'administracion/horarios_soporte.html'

    def test_func(self):
        return self.request.user.usuariosgrexco.tipo == 'A'


class CrearHorariosSoporte(LoginRequiredMixin, UserPassesTestMixin, View):
    """Vista para consultar los horarios de soporte por Empresa."""
    login_url = 'usuarios:login'

    def test_func(self):
        """Restringe el acceso solo a usuario administrador."""
        return self.request.user.usuariosgrexco.tipo == 'A'

    def post(self, request, *args, **kwargs):
        data = dict(request.POST)
        nit_empresa = data['selEmpresa'][0]
        horarios = []

        # Recorre el diccionario con los datos de los horarios
        # y crea una lista Modelos creados con estos datos.
        if Empresas.objects.filter(nit=nit_empresa):
            empresa = Empresas.objects.get(nit=nit_empresa)
            print(data)
            for k, v in data.items():
                # Las variables: hora_inicio y hora_fin son listas con el
                # formato: [hora, minuto]
                #
                # Lunes
                if k == 'inicio-lunes':
                    if v[0]:
                        hora_inicio = [int(v[0][:2]), int(v[0][3:])]
                        hora_fin = [
                            int(data['fin-lunes'][0][:2]),
                            int(data['fin-lunes'][0][3:])
                        ]
                        lunes = HorariosSoporte(
                            dia=0,
                            descripcion='Lunes',
                            inicio=time(
                                hour=hora_inicio[0], minute=hora_inicio[1]),
                            fin=time(hour=hora_fin[0], minute=hora_fin[1])
                        )
                    else:
                        lunes = HorariosSoporte(
                            dia=0,
                            descripcion='Lunes',
                            inicio=None,
                            fin=None
                        )
                    horarios.append(lunes)
                #
                # Martes
                elif k == 'inicio-martes':
                    if v[0]:
                        hora_inicio = [int(v[0][:2]), int(v[0][3:])]
                        hora_fin = [
                            int(data['fin-martes'][0][:2]),
                            int(data['fin-martes'][0][3:])
                        ]
                        martes = HorariosSoporte(
                            dia=1,
                            descripcion='Martes',
                            inicio=time(hour=hora_inicio[0], minute=hora_inicio[1]),
                            fin=time(hour=hora_fin[0], minute=hora_fin[1])
                        )
                    else:
                        martes = HorariosSoporte(
                            dia=1,
                            descripcion='Martes',
                            inicio=None,
                            fin=None
                        )
                    horarios.append(martes)
                #
                # Miercoles
                elif k == 'inicio-miercoles':
                    if v[0]:
                        hora_inicio = [int(v[0][:2]), int(v[0][3:])]
                        hora_fin = [
                            int(data['fin-miercoles'][0][:2]),
                            int(data['fin-miercoles'][0][3:])
                        ]
                        miercoles = HorariosSoporte(
                            dia=2,
                            descripcion='Miercoles',
                            inicio=time(hour=hora_inicio[0], minute=hora_inicio[1]),
                            fin=time(hour=hora_fin[0], minute=hora_fin[1])
                        )
                    else:
                        miercoles = HorariosSoporte(
                            dia=2,
                            descripcion='Miercoles',
                            inicio=None,
                            fin=None
                        )
                    horarios.append(miercoles)
                #
                # Jueves
                elif k == 'inicio-jueves':
                    if v[0]:
                        hora_inicio = [int(v[0][:2]), int(v[0][3:])]
                        hora_fin = [
                            int(data['fin-jueves'][0][:2]),
                            int(data['fin-jueves'][0][3:])
                        ]
                        jueves = HorariosSoporte(
                            dia=3,
                            descripcion='Jueves',
                            inicio=time(hour=hora_inicio[0], minute=hora_inicio[1]),
                            fin=time(hour=hora_fin[0], minute=hora_fin[1])
                        )
                    else:
                        jueves = HorariosSoporte(
                            dia=3,
                            descripcion='Jueves',
                            inicio=None,
                            fin=None
                        )
                    horarios.append(jueves)
                #
                # Viernes
                elif k == 'inicio-viernes':
                    if v[0]:
                        hora_inicio = [int(v[0][:2]), int(v[0][3:])]
                        hora_fin = [
                            int(data['fin-viernes'][0][:2]),
                            int(data['fin-viernes'][0][3:])
                        ]
                        viernes = HorariosSoporte(
                            dia=4,
                            descripcion='Viernes',
                            inicio=time(hour=hora_inicio[0], minute=hora_inicio[1]),
                            fin=time(hour=hora_fin[0], minute=hora_fin[1])
                        )
                    else:
                        viernes = HorariosSoporte(
                            dia=4,
                            descripcion='Viernes',
                            inicio=None,
                            fin=None
                        )
                    horarios.append(viernes)
                #
                # Sabado
                elif k == 'inicio-sabado':
                    if v[0]:
                        hora_inicio = [int(v[0][:2]), int(v[0][3:])]
                        hora_fin = [
                            int(data['fin-sabado'][0][:2]),
                            int(data['fin-sabado'][0][3:])
                        ]
                        sabado = HorariosSoporte(
                            dia=5,
                            descripcion='Sabado',
                            inicio=time(hour=hora_inicio[0], minute=hora_inicio[1]),
                            fin=time(hour=hora_fin[0], minute=hora_fin[1])
                        )
                    else:
                        sabado = HorariosSoporte(
                            dia=5,
                            descripcion='Sabado',
                            inicio=None,
                            fin=None
                        )
                    horarios.append(sabado)
                #
                # Domingo
                elif k == 'inicio-domingo':
                    if v[0]:
                        hora_inicio = [int(v[0][:2]), int(v[0][3:])]
                        hora_fin = [
                            int(data['fin-domingo'][0][:2]),
                            int(data['fin-domingo'][0][3:])
                        ]
                        domingo = HorariosSoporte(
                            dia=6,
                            descripcion='Domingo',
                            inicio=time(hour=hora_inicio[0], minute=hora_inicio[1]),
                            fin=time(hour=hora_fin[0], minute=hora_fin[1])
                        )
                    else:
                        domingo = HorariosSoporte(
                            dia=6,
                            descripcion='Domingo',
                            inicio=None,
                            fin=None
                        )
                    horarios.append(domingo)
                else:
                    pass
        else:
            return JsonResponse({'error': 'La empresa no existe'}, status=400)

        with transaction.atomic():
            try:
                for horario in horarios:
                    horario.save()
                    empresa.horariossoporte_set.add(horario)
            except Exception as e:
                return JsonResponse(
                    {'error': 'Ocurrió un error: {}'.format(e)}, status=400)

            return JsonResponse(
                {'ok': 'Se guardaron los datos correctamente'}, status=200)


class ConsultaHorariosSoporte(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Vista para consultar el detalle de los horarios de soporte de una Empresa.
    """
    login_url = 'usuarios:login'
    template_name = 'administracion/horarios_soporte_consulta.html'

    def test_func(self):
        return self.request.user.usuariosgrexco.tipo == 'A'

    def get_context_data(self, **kwargs):
        nit = kwargs['nit']
        qry_empresa = get_object_or_404(Empresas, nit=nit)
        qry_horarios = qry_empresa.horariossoporte_set.values()
        empresa = {'nombre': qry_empresa.nombre, 'nit': qry_empresa.nit}
        info_horarios = {'empresa': empresa, 'horarios': qry_horarios}

        return {'horarios': info_horarios}


# ............................................................................
#                     PRIORIDADES DE RESPUESTA                               .
# ............................................................................
class PrioridadesRespuestaView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Vista que retorna un Json con los datos de las prioridades de respuesta
    """
    login_url = 'usuarios:login'

    def test_func(self):
        return self.request.user.usuariosgrexco.tipo == 'A'

    def get(self, request):
        qry_prio_respuesta = PrioridadesRespuesta.objects.values().all()
        prioridades = []
        for prioridad in qry_prio_respuesta:
            prioridades.append(prioridad)

        return JsonResponse({'prioridades': prioridades}, status=200)


# ............................................................................
#                         TIEMPOS DE RESPUESTA                               .
# ............................................................................
class TiemposRespuestaView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Vista para consultar los tiempos de respuesta por empresa.
    """
    login_url = 'usuarios:login'
    template_name = 'administracion/tiempos_respuesta.html'

    def test_func(self):
        return self.request.user.usuariosgrexco.tipo == 'A'


class TiemposRespuestaEmpresas(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Retorna un listado de las empresas que tienen Tiempos de
    respuesta asignados.

    Select Distinct administracion_empresas.nit,
        administracion_tiemposrespuesta.empresa_id
    From administracion_empresas, administracion_tiemposrespuesta
    Where administracion_empresas.nit =
        administracion_tiemposrespuesta.empresa_id;

    """
    login_url = 'usuarios:login'

    def test_func(self):
        return self.request.user.usuariosgrexco.tipo == 'A'

    def get(self, request, *args, **kwargs):
        qry_empresas = (
            Empresas.objects
                    .filter(tiempos_respuesta__empresa__isnull=False)
                    .values('nit', 'nombre')
                    .distinct()
        )
        empresas = []
        for empresa in qry_empresas:
            empresas.append(empresa)

        return JsonResponse({'empresas': empresas}, status=200)


class CrearTiemposRespuestaView(
        LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Vista para guardar/actualizar los tiempos de respuesta.
    """
    login_url = 'usuarios:login'

    def test_func(self):
        return self.request.user.usuariosgrexco.tipo == 'A'

    def post(self, request, *args, **kwargs):
        data = dict(request.POST)
        # print(data)
        nit = data['empresa'][0]

        # Verifica que la empresa exista
        if Empresas.objects.filter(nit=nit):
            empresa = Empresas.objects.get(nit=nit)

            # Si la empresa tiene datos en la tabla de Tiempos de respuesta
            # actualiza esta información, si no entonces los crea.
            if empresa.tiempos_respuesta.values('prioridad'):
                with transaction.atomic():

                    # Alta
                    tr = empresa.tiempos_respuesta.get(prioridad='A')
                    tr.tiempo = int(data['alta'][0])
                    tr.save()

                    # Media
                    tr = empresa.tiempos_respuesta.get(prioridad='M')
                    tr.tiempo = int(data['media'][0])
                    tr.save()

                    # Baja
                    tr = empresa.tiempos_respuesta.get(prioridad='B')
                    tr.tiempo = int(data['baja'][0])
                    tr.save()
                    return JsonResponse(
                        {'ok': 'Se grabaron correctamente todos los datos'},
                        status=200)
            else:
                with transaction.atomic():
                    for k, v in data.items():
                        if k == 'alta':
                            prioridad = PrioridadesRespuesta(codigo='A')
                            hora = int(v[0])
                            TiemposRespuesta.objects.create(
                                empresa=empresa,
                                prioridad=prioridad,
                                tiempo=hora
                            )
                        elif k == 'media':
                            prioridad = PrioridadesRespuesta(codigo='M')
                            hora = int(v[0])
                            TiemposRespuesta.objects.create(
                                empresa=empresa,
                                prioridad=prioridad,
                                tiempo=hora
                            )
                        elif k == 'baja':
                            prioridad = PrioridadesRespuesta(codigo='B')
                            hora = int(v[0])
                            TiemposRespuesta.objects.create(
                                empresa=empresa,
                                prioridad=prioridad,
                                tiempo=hora
                            )
                        else:
                            continue
                    return JsonResponse(
                        {'ok': 'Se grabaron correctamente todos los datos'},
                        status=200)
        else:
            return JsonResponse({'error': 'La empresa no existe'}, status=400)


class ConsultaTiemposRespuestaView(
        LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Vista para consultar los tiempos de respuesta por empresa.
    """

    login_url = 'usuarios:login'
    template_name = 'administracion/tiempos_respuesta_detalle.html'

    def test_func(self):
        return self.request.user.usuariosgrexco.tipo == 'A'

    def get_context_data(self, **kwargs):
        nit = kwargs['nit']
        # print(nit)
        qry_empresa = get_object_or_404(Empresas, nit=nit)
        qry_tiempos_respuesta = TiemposRespuesta.objects.filter(empresa=nit).all()

        return {'tiempos': qry_tiempos_respuesta, 'empresa': qry_empresa}


# ............................................................................
# .                            Empresas                                      .
# ............................................................................
class CompaniesView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Vista consultar empresas
    """
    login_url = 'usuarios:login'
    template_name = 'administracion/empresas.html'

    def test_func(self):
        return self.request.user.usuariosgrexco.tipo == 'A'

    def get_context_data(self, *args, **kwargs):
        empresas = Empresas.objects.all()
        plataformas = Plataformas.objects.all()
        aplicaciones = Aplicaciones.objects.all()

        return {
            'empresas': empresas, 'plataformas': plataformas,
            'aplicaciones': aplicaciones}


class CrearEmpresaView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Vista para crear empresas."""
    login_url = 'usuarios:login'

    def test_func(self):
        return self.request.user.usuariosgrexco.tipo == 'A'

    def post(self, request, *args, **kwargs):
        """docstring."""
        data = dict(request.POST)
        nit = data['nit'][0]
        nombre = data['nombre'][0]
        direccion = data['direccion'][0]
        telefono = data['telefono'][0]
        activa = data['activa'][0]
        id_plataforma = int(data['plataforma'][0])

        # Verifica que no hayan campos en blanco.
        for k, v in data.items():
            if len(data[k][0]) == 0:
                mensaje = 'El campo {} esta vacio'.format(k.capitalize())
                return JsonResponse({'error': mensaje}, status=400)
                break

        if id_plataforma == 0:
            return JsonResponse(
                {'error': 'Debe seleccionar una plataforma'}, status=400)

        plataforma = Plataformas.objects.get(id=id_plataforma)
        empresa = Empresas(
            nit=nit, nombre=nombre, direccion=direccion, telefono=telefono,
            activa=activa, plataforma=plataforma
        )

        with transaction.atomic():
            try:
                empresa.save()
            except Exception as e:
                return JsonResponse({"error": e}, status=400)

            return JsonResponse(
                {"ok": "Los datos de guardaron correctamente."})


class ConsultaEmpresaView(
        LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Renderiza un template para consultar la información de una Empresa.

    """
    login_url = 'usuarios:login'
    template_name = 'administracion/empresas_detalle.html'

    def test_func(self):
        """docstring."""
        return self.request.user.usuariosgrexco.tipo == 'A'

    def get_context_data(self, **kwargs):
        nit = kwargs['nit']
        qry_empresa = get_object_or_404(Empresas, nit=nit)
        qry_convenios = qry_empresa.convenios.all()
        return {'empresa': qry_empresa, 'convenios': qry_convenios}


class DetalleEmpresaView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Retorna un JSON con la información de la empresa seleccionada."""
    login_url = 'usuarios:login'
    template_name = 'administracion/empresas_detalle.html'

    def test_func(self):
        """docstring."""
        return self.request.user.usuariosgrexco.tipo == 'A'

    def get(self, request, *args, **kwargs):
        nit = kwargs['nit']
        qry_empresa = get_object_or_404(Empresas, nit=nit)
        return JsonResponse({'empresa': nit}, status=200)


class ListadoBasicoEmpresasView(
        LoginRequiredMixin, UserPassesTestMixin, View):
    """Retorna un listado con los datos basicos de las Empresas."""

    login_url = 'usuarios:login'

    def test_func(self):
        """docstring."""
        return self.request.user.usuariosgrexco.tipo == 'A'

    def get(self, request, *args, **kwargs):
        """docstring."""
        qry_empresas = (
            Empresas.objects
                    .values(
                        'nit', 'nombre', 'direccion', 'telefono', 'activa',
                        'plataforma__nombre')
                    .all()
        )
        empresas = []
        for empresa in qry_empresas:
            if empresa['activa'] is True:
                empresa['activa'] = 'Si'
            else:
                empresa['activa'] = 'No'
            empresas.append(empresa)

        return JsonResponse({'empresas': empresas}, status=200)


class ListadoEmpresasActivas(LoginRequiredMixin, UserPassesTestMixin, View):
    """Retorna un listado con los datos basicos de las empresas activas."""

    login_url = 'usuarios:login'

    def test_func(self):
        """Restringe el acceso solo a usuario administrador."""
        return self.request.user.usuariosgrexco.tipo == 'A'

    def get(self, request, *args, **kwargs):
        """docstring."""
        qry_empresas = (
            Empresas.objects
                    .filter(activa=True)
                    .values(
                        'nit', 'nombre', 'direccion', 'telefono', 'activa',
                        'plataforma__nombre')
                    .all()
        )
        empresas = []
        for empresa in qry_empresas:
            if empresa['activa'] is True:
                empresa['activa'] = 'Si'
            else:
                empresa['activa'] = 'No'
            empresas.append(empresa)

        return JsonResponse({'empresas': empresas}, status=200)



class ActualizaEmpresaView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Permite actualizar la información de la empresa."""

    login_url = 'usuarios:login'

    def test_func(self):
        """Restringe el acceso solo a usuario administrador."""
        return self.request.user.usuariosgrexco.tipo == 'A'

    def post(self, request):
        data = dict(request.POST)
        nit = data['nit'][0]
        direccion = data['direccion'][0]
        telefono = data['telefono'][0]
        id_plataforma = int(data['plataforma'][0])
        empresa = get_object_or_404(Empresas, nit=nit)

        if empresa_activa(nit):
            pass
        else:
            return JsonResponse(
                {'error': 'La empresa esta inactiva'}, status=400)

        if direccion:
            empresa.direccion = direccion

        if telefono:
            empresa.telefono = telefono

        print(id_plataforma, type(id_plataforma))
        if id_plataforma == 0:
            print('1')
        else:
            print('2')
            plataforma = get_object_or_404(Plataformas, id=id_plataforma)
            empresa.plataforma = plataforma

        with transaction.atomic():
            try:
                empresa.save()
            except Exception as e:
                return JsonResponse({'error': e}, status=400)

        return JsonResponse({'ok': 'Se actualizó la información'}, status=200)


class ActivaEmpresasView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Activa empresas. """

    login_url = 'usuarios:login'

    def test_func(self):
        """Restringe el acceso solo a usuario administrador."""
        return self.request.user.usuariosgrexco.tipo == 'A'

    def post(self, request):
        data = dict(request.POST)
        nit = data['nit'][0]
        empresa = get_object_or_404(Empresas, nit=nit)

        with transaction.atomic():
            if empresa.activa is False:
                empresa.activa = True
            else:
                return JsonResponse(
                    {'error': 'La empresa se encuentra activa'},
                    status=400
                )

            try:
                empresa.save()
            except Exception as e:
                return JsonResponse({'error': e}, status=400)

            return JsonResponse({'ok': 'ok'}, status=200)


class DesactivaEmpresasView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Permite desactivar una empresa."""

    login_url = 'usuarios:login'

    def test_func(self):
        """Restringe el acceso solo a usuario administrador."""
        return self.request.user.usuariosgrexco.tipo == 'A'

    def post(self, request):
        data = dict(request.POST)
        nit = data['nit'][0]
        empresa = get_object_or_404(Empresas, nit=nit)

        with transaction.atomic():
            if empresa.activa:
                empresa.activa = False
            else:
                return JsonResponse(
                    {'error': 'La empresa ya se encuentra inactiva'},
                    status=400
                )

            try:
                empresa.save()
            except Exception as e:
                return JsonResponse({'error': e}, status=400)

            return JsonResponse({'ok': 'ok'}, status=200)


# ............................................................................
# .                            Convenios                                     .
# ............................................................................
class ConveniosView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Vista para consultar los convenios organizados por Empresa.

    url = convenios/
    """

    login_url = 'usuarios:login'
    template_name = 'administracion/convenios.html'

    def test_func(self):
        """Restringe el acceso solo a usuario administrador."""
        return self.request.user.usuariosgrexco.tipo == 'A'


class CrearConveniosView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Vista para crear convenios.

    url = convenios/nuevo/
    """

    login_url = 'usuarios:login'

    def test_func(self):
        """Restringe el acceso solo a usuario administrador."""
        return self.request.user.usuariosgrexco.tipo == 'A'

    def post(self, request, *args, **kwargs):
        """docstring."""
        data = json.loads(request.body.decode('utf-8'))
        nit_empresa = data['empresa']
        aplicaciones = data['aplicaciones']

        # Verifica si la empresa existe
        if Empresas.objects.filter(nit=nit_empresa):
            empresa = Empresas.objects.get(nit=nit_empresa)
        else:
            return JsonResponse({'error': 'La empresa no existe'}, status=400)

        # verifica si la empresa esta activa
        if empresa_activa(nit_empresa):
            pass
        else:
            return JsonResponse(
                {'error': 'La empresa esta inactiva'}, status=400)

        # Verifica si la empresa ya tiene convenios
        if empresa.convenios.all():
            mensaje = """ La empresa '{}' ya tiene convenios.
                          Si desea modificarlos por favor consulte la
                          empresa y actualice la información.
                      """.format(empresa.nombre)
            return JsonResponse({'error': mensaje}, status=400)

        with transaction.atomic():
            for app in aplicaciones:
                aplicacion = get_object_or_404(Aplicaciones, id=app['id'])
                Convenios.objects.create(
                    empresa=empresa, aplicacion=aplicacion)

            return JsonResponse(
                {'ok': 'Se crearon todos los convenios'}, status=200)


class ConsultaConveniosView(
        LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Template para consultar una empresa y sus convenios.

    """

    login_url = 'usuarios:login'
    template_name = 'administracion/convenios_consulta.html'

    def test_func(self):
        """Restringe el acceso solo a usuario administrador."""
        return self.request.user.usuariosgrexco.tipo == 'A'

    def get_context_data(self, **kwargs):
        """docstring."""
        nit = kwargs['nit']
        qry_empresa = get_object_or_404(Empresas, nit=nit)
        qry_convenios = qry_empresa.convenios.all()

        return {'empresa': qry_empresa, 'convenios': qry_convenios}


class ActualizarConveniosView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Agrega los convenios recibidos ya existentes."""
    login_url = 'usuarios:login'

    def test_func(self):
        """Restringe el acceso solo al usuario administrador."""
        return self.request.user.usuariosgrexco.tipo == 'A'

    def post(self, request):
        """docstring."""
        data = json.loads(request.body.decode('utf-8'))
        nit_empresa = data['empresa']
        aplicaciones = data['aplicaciones']

        # Verifica si la empresa existe
        if Empresas.objects.filter(nit=nit_empresa):
            empresa = Empresas.objects.get(nit=nit_empresa)

            # Verifica si la empresa esta activa
            if empresa_activa(nit_empresa):
                pass
            else:
                return JsonResponse(
                    {'error': 'La empresa esta inactiva'}, status=400)

            with transaction.atomic():
                for aplicacion in aplicaciones:
                    app = Aplicaciones.objects.get(id=aplicacion['id'])
                    convenio = Convenios(empresa=empresa, aplicacion=app)
                    try:
                        convenio.save()
                    except Exception as e:
                        return JsonResponse(
                            {'error': 'Ocurrió un error: %s' % (e)},
                            status=400
                        )
                        break

                return JsonResponse(
                    {'ok': 'Se guardó la información correctamente'},
                    status=200
                )
        else:
            return JsonResponse({'error': 'La empresa no existe'}, status=400)


class EliminaConveniosView(LoginRequiredMixin, UserPassesTestMixin, View):
    """pass."""
    pass


class ListadoConveniosEmpresasView(
        LoginRequiredMixin, UserPassesTestMixin, View):
    """Retorna un listado de Empresas que tengan Convenios."""

    login_url = 'usuarios:login'

    def test_func(self):
        """Restringe el acceso solo al usuario administrador."""
        return self.request.user.usuariosgrexco.tipo == 'A'

    def get(self, request):
        """docstring."""
        qry_empresas = (
            Empresas.objects
                    .filter(convenios__empresa__isnull=False)
                    .values('nit', 'nombre')
                    .distinct()
                    .all()
        )
        empresas = []

        for empresa in qry_empresas:
            empresas.append(empresa)

        return JsonResponse({'empresas': empresas}, status=200)


class ListadoNoConveniosEmpresasView(
        LoginRequiredMixin, UserPassesTestMixin, View):
    """Retorna un JSON con las aplicaciones que no pertencen a la empresa."""

    login_url = 'usuarios:login'

    def test_func(self):
        """Restringe el acceso solo al usuario administrador."""
        return self.request.user.usuariosgrexco.tipo == 'A'

    def get(self, request, **kwargs):
        nit = kwargs['nit']

        if Empresas.objects.filter(nit=nit):
            qry_sql = """
                SELECT administracion_aplicaciones.id,
                       administracion_aplicaciones.nombre
                FROM administracion_aplicaciones
                WHERE administracion_aplicaciones.id NOT IN
                (
                    SELECT administracion_convenios.aplicacion_id
                    FROM administracion_convenios
                    WHERE administracion_convenios.empresa_id = '%s'
                )
                ORDER BY administracion_aplicaciones.id;""" % (nit)

            with connection.cursor() as cursor:
                cursor.execute(qry_sql)
                aplicaciones = sql_a_diccionario(cursor)

            return JsonResponse({'aplicaciones': aplicaciones}, status=200)
        else:
            return JsonResponse(
                {'error': 'La empresa no existe'},
                status=400
            )


# ............................................................................
# .                             Usuarios                                     .
# ............................................................................
class CrearUsuariosView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Vista para crear Usuarios.

    El orden para crear un usuario:
        1. Tener creada la: Empresa
        2. User
        3. UsuariosGrexco

    """

    login_url = 'usuarios:login'
    template_name = 'administracion/nuevo_usuario.html'

    def test_func(self):
        return self.request.user.usuariosgrexco.tipo == 'A'

    def get_context_data(self):
        empresas = Empresas.objects.all()
        return {'empresas': empresas}

    def post(self, request, *args, **kwargs):
        data = dict(request.POST)
        nombre_usuario = data['nombre_usuario'][0]
        tipo = data['tipo_usuario'][0]

        # Verifica si el nombre de usuario existe.
        if User.objects.filter(username=nombre_usuario):
            user = get_object_or_404(username=nombre_usuario)
            return JsonResponse(
                {'error': 'El nombre de usuario ya existe'},
                status=400
            )

        if tipo == 'cliente':
            try:
                user = User.objects.create_user(
                    username=data['nombre_usuario'][0],
                    password='123456',
                    email=data['email'][0],
                    first_name=data['nombre'][0],
                    last_name=data['apellido'][0],
                )
            except Exception as e:
                return JsonResponse(
                    {"error": "Ocurrio un error al crear el usuario: {}".format(e)},
                    status=400,
                )

            empresa = Empresas.objects.get(nit=data['empresa'][0])
            ug = UsuariosGrexco(
                user_id=user,
                tipo='C',
                telefono=data['telefono'][0],
                extension=data['extension'][0],
                cargo=data['cargo'][0],
                empresas_nit=empresa
            )
            try:
                ug.save()
            except Exception as e:
                mensaje = "Ocurrio un error al guardar el tipo de usuario: {}".format(e)
                print(e)
                user.delete()
                return JsonResponse(
                    {"error": mensaje},
                    status=400,
                )

            mensaje = "Se creo el usuario {}".format(ug.user_id.username)
            print(mensaje)
            return JsonResponse({'ok': mensaje})
        elif tipo_usuario == 'soporte':
            try:
                user = User.objects.create_user(
                    username=data['nombre_usuario'][0],
                    password='grexco02',
                    email=data['email'][0],
                    first_name=data['nombre'][0],
                    last_name=data['apellido'][0],
                )
            except Exception as e:
                print(e)
                return JsonResponse(
                    {"error": "Ocurrio un error al crear el usuario: {}".format(e)},
                    status=400,
                )

            empresa = Empresas.objects.get(nit='8000497311')
            if data['es-coordinador'][0] == 'on':
                ug = UsuariosGrexco(
                    user_id=user,
                    tipo='C',
                    extension=data['extension'][0],
                    cargo='Soporte',
                    empresas_nit=empresa,
                    es_coordinador=True,
                )
            else:
                ug = UsuariosGrexco(
                    user_id=user,
                    tipo='C',
                    extension=data['extension'][0],
                    cargo='Soporte',
                    empresas_nit=empresa,
                    es_coordinador=False,
                )
            try:
                ug.save()
            except Exception as e:
                mensaje = "Ocurrio un error al guardar el tipo de usuario: {}".format(e)
                print(e)
                user.delete()
                return JsonResponse(
                    {"error": mensaje},
                    status=400,
                )

            mensaje = "Se creo el usuario {}".format(ug.user_id.username)
            print(mensaje)
            return JsonResponse({'ok': mensaje})
        elif tipo_usuario == 'tecnologia':
            try:
                user = User.objects.create_user(
                    username=data['nombre_usuario'][0],
                    password='grexco02',
                    email=data['email'][0],
                    first_name=data['nombre'][0],
                    last_name=data['apellido'][0],
                )
            except Exception as e:
                print(e)
                return JsonResponse(
                    {"error": "Ocurrio un error al crear el usuario: {}".format(e)},
                    status=400,
                )

            empresa = Empresas.objects.get(nit='8000497311')
            if data['es-coordinador'][0] == 'on':
                ug = UsuariosGrexco(
                    user_id=user,
                    tipo='C',
                    extension=data['extension'][0],
                    cargo='Tecnologia',
                    empresas_nit=empresa,
                    es_coordinador=True,
                )
            else:
                ug = UsuariosGrexco(
                    user_id=user,
                    tipo='C',
                    extension=data['extension'][0],
                    cargo='Soporte',
                    empresas_nit=empresa,
                    es_coordinador=False,
                )

            try:
                ug.save()
            except Exception as e:
                mensaje = "Ocurrio un error al guardar el tipo de usuario: {}".format(e)
                print(e)
                user.delete()
                return JsonResponse(
                    {"error": mensaje},
                    status=400,
                )

            mensaje = "Se creo el usuario {}".format(ug.user_id.username)
            print(mensaje)
            return JsonResponse({'ok': mensaje})



class ConsultClientsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    login_url = 'usuarios:login'
    template_name = 'administracion/clientes.html'

    def test_func(self):
        return self.request.user.usuariosgrexco.tipo == 'A'

    def get_context_data(self, *args, **kwargs):
        clientes = UsuariosGrexco.objects.filter(tipo='C')
        return {'clientes': clientes}

    def post(self, request, *args, **kwargs):
        data = dict(request.POST)
        nombre_usuario = data['nombre_usuario'][0]
        usr = UsuariosGrexco.objects.filter(user_id__username=nombre_usuario)
        print(usr)
        usuario = serializers.serialize('json', usr)
        print(usuario)
        return HttpResponse(usuario, content_type='application/json')