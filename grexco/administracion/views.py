import json
import pyexcel as pe

from datetime import time

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db import transaction
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from administracion.models import Aplicaciones
from administracion.models import Convenios
from administracion.models import Empresas
from administracion.models import HorariosSoporte
from administracion.models import Plataformas
from administracion.models import PrioridadesRespuesta
from administracion.models import Reportes
from administracion.models import TiemposRespuesta
from administracion.models import UsuariosGrexco


# Create your views here.
def genera_id(modelo):
    """
    Recibe como parametro un Model de:
        administracion.Models
    """
    x = modelo.objects.last()
    if x is None:
        return 1
    else:
        return x.id + 1


class LoginView(TemplateView):
    """docstring for LoginView"""
    template_name = 'administracion/login.html'

    def post(self, request):
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


# ****************************************************************************
# *                            Plataformas                                   *
# ****************************************************************************
class PlatformView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Vista para consultar plataformas
    """
    login_url = 'administracion:admin_login'
    template_name = 'administracion/plataformas.html'

    def test_func(self):
        return self.request.user.usuariosgrexco.tipo == 'A'

    def get_context_data(self, *args, **kwargs):
        plataforma = Plataformas.objects.all()

        return {'plataformas': plataforma}


class CreatePlatformView(
        LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Vista para crear plataformas
    """
    login_url = 'usuarios:login'
    template_name = 'administracion/nueva_plataforma.html'

    def test_func(self):
        return self.request.user.usuariosgrexco.tipo == 'A'

    def post(self, request, *args, **kwargs):
        data = dict(request.POST)
        nombre = data['nombre'][0]
        version = data['version'][0]

        if not nombre or not version:
            return JsonResponse(
                {"error": "Los campos estan vacios"}, status=400)

        plataforma = Plataformas.objects.filter(
            nombre=nombre.upper(), version=version.upper())

        if plataforma.exists():
            return JsonResponse({"error": "Los datos ya existen"}, status=400)
        else:
            id = Plataformas.objects.values('id').last()['id'] + 1
            plt = Plataformas(id=id, nombre=nombre.upper(), version=version)
            try:
                plt.save()
            except Exception as e:
                mensaje = "Ocurrio un error al grabar los datos: {}".format(e)
                return JsonResponse({"error": mensaje}, status=400)

            mensaje = "Se guardo la plataforma: {}".format(plt)
            return JsonResponse({"ok": mensaje})


class DeletePlatformView(
        LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Vista para eliminar plataformas
    """
    login_url = 'usuarios:login'
    template_name = 'administracion/companies.html'

    def test_func(self):
        return self.request.user.usuariosgrexco.tipo == 'A'

    def post(self, request, *args, **kargs):
        data = dict(request.POST)
        for k, v in data.items():
            plataforma = Plataformas.objects.get(id=int(data[k][0]))
            if plataforma:
                from django.db.models.deletion import ProtectedError
                try:
                    plataforma.delete()
                except ProtectedError as e:
                    empresa = Empresas.objects.get(plataforma__id=plataforma.id)
                    msj = 'No es posible eliminar: {}-{}. Pertenece a la empresa: {}'.format(
                        plataforma.nombre, plataforma.version, empresa.nombre,)
                    return JsonResponse({"error": msj}, status=400)

        mensaje = 'Se eliminó la plataforma: {}'.format(plataforma.nombre)
        return JsonResponse({"ok": mensaje}, status=200)


# ****************************************************************************
# *                                Aplicaciones                              *
# ****************************************************************************
class AplicationsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Vista para consultar las aplicaciones
    """
    login_url = 'usuarios:login'
    template_name = 'administracion/aplicaciones.html'

    def test_func(self):
        return self.request.user.usuariosgrexco.tipo == 'A'

    def get_context_data(self, *args, **kwargs):
        aplicaciones = Aplicaciones.objects.all()
        return {'aplicaciones': aplicaciones}

    def post(self, request, *args, **kwargs):
        """
        Retorna la información de: Versión y Convenios, de la aplicación
        seleccionada.
        """
        data = dict(request.POST)
        id = data['id'][0]
        app = Aplicaciones.objects.get(id=id)

        convenios = []
        qry_convenios = app.convenios.values('empresa__nombre', 'empresa__nit').all()
        if len(qry_convenios) == 0:
            dic_convenios = {'empresa': 'Esta aplicación no es usada por ningún Cliente.'}
            convenios.append(dic_convenios)
        else:
            for convenio in qry_convenios:
                dic_convenios = {}
                dic_convenios['empresa'] = convenio['empresa__nombre']
                dic_convenios['nit'] = convenio['empresa__nit']
                convenios.append(dic_convenios)

        versiones = []
        qry_versiones = app.versiones.values('version', 'fecha').all().order_by('-version')
        if len(qry_versiones) == 0:
            dic_versiones = {'version': 'No tiene versiones', 'fecha': 'No tiene versiones'}
            versiones.append(dic_versiones)
        else:
            for ver in qry_versiones:
                dic_versiones = {}
                dic_versiones['version'] = ver['version']
                dic_versiones['fecha'] = ver['fecha'].strftime(format='%Y-%m-%d')
                versiones.append(dic_versiones)

        aplicacion = {'aplicacion': app.nombre, 'versiones': versiones, 'convenios': convenios}
        # print(aplicacion)
        return JsonResponse({'aplicacion': aplicacion}, status=200)


class CreateAplicationsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Vista para crear Aplicaciones
    """
    login_url = 'usuarios:login'

    def test_func(self):
        return self.request.user.usuariosgrexco.tipo == 'A'

    def post(self, request, *args, **kwargs):
        """
        Si POST trae datos se crea la aplicacion por formulario, si no
        entonces, por archivo Excel.
        """
        data = request.POST
        if len(data) == 1:
            id = genera_id(Aplicaciones)
            nombre = data['nombre']
            app = Aplicaciones(id=id, nombre=nombre)

            if Aplicaciones.objects.filter(nombre=nombre).exists():
                return JsonResponse({'error': 'La aplicación: {}. Ya existe.'.format(nombre)}, status=400)

            try:
                app.save()
            except Exception as e:
                return JsonResponse({'error': 'Ocurrio un error {}'.format(e)}, status=400)

            return JsonResponse({'ok': 'Se creo la aplicación: {}'.format(nombre)}, status=200)
        else:
            file = request.FILES['archivo']
            file_type = file.name.split('.')[-1]
            cuenta_guardados = 0
            no_grabados = []
            data = pe.iget_records(file_stream=file, file_type=file_type)
            n_columnas = pe.get_sheet(file_stream=file, file_type=file_type).number_of_rows() - 1
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
                        return JsonResponse({'error': 'Ocurrio un error: {}'.format(e)}, status=400)

                    cuenta_guardados = cuenta_guardados + 1

            if cuenta_guardados == n_columnas:
                return JsonResponse({'ok': 'Se grabaron todas las Aplicaciones'}, status=200)
            else:
                respuesta = "Se grabaron {} de {}".format(cuenta_guardados, n_columnas)
                return JsonResponse({'error': {'respuesta': respuesta, 'aplicaciones': no_grabados}}, safe=False, status=400)


class DeleteAplicationsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Vista para eliminar Aplicaciones.
    Solo si la aplicación no tiene versiones, convenios o reportes.
    """
    login_url = 'usuarios:login'

    def test_func(self):
        return self.request.user.usuariosgrexco.tipo == 'A'

    def post(self, request, *args, **kwargs):
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

        if len(convenios) > 0 or len(versiones) > 0 or len(reportes):
            return JsonResponse(
                {'error': 'No es posible eliminar {}. Está siendo usada'.format(app.nombre)},
                status=400
            )
        else:
            app.delete()
            return JsonResponse(
                {'ok': 'Se eliminó la aplicación: {}'.format(app.nombre)},
                status=200)


class ListAplicationsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Retorna un JSON con la información (id y nombre) de la aplicación o
    un archivo de Excel con la misma información dependiendo del 'tipo' que
    se envie en los parametros que se pasen en el POST al momento
    de hacer el Request:

    tipo = listado --> JSON
    tipo = excel   --> Excel

    """
    login_url = 'usuarios:login'

    def test_func(self):
        return self.request.user.usuariosgrexco.tipo == 'A'

    def post(self, request, *args, **kwargs):
        data = dict(request.POST)
        tipo = data['tipo'][0]

        if tipo == 'listado':
            qry_aplicaciones = Aplicaciones.objects.values('id', 'nombre').all().order_by('id')
            aplicaciones = []
            for aplicacion in qry_aplicaciones:
                aplicaciones.append(aplicacion)

            return JsonResponse(aplicaciones, status=200, safe=False)


class ListExcelAplicationsView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Retorna un archivo de excel con el listado de las aplicaciones.
    """
    login_url = 'usuarios:login'

    def test_func(self):
        return self.request.user.usuariosgrexco.tipo == 'A'

    def get(self, request, *args, **kwargs):
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
    """
    Vista reportes
    """
    login_url = 'usuarios:login'
    template_name = 'administracion/reportes.html'

    def test_func(self):
        return self.request.user.usuariosgrexco.tipo == 'A'

    def post(self, request, *args, **kwargs):
        qry_reportes = Reportes.objects.values(
            'id', 'nombre', 'aplicacion__nombre').all()
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
        return self.request.user.usuariosgrexco.tipo == 'A'

    def post(self, request, *args, **kwargs):
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
                    {"error": "¡El reporte '{}' ya existe!".format(reporte.nombre)}, status=400)

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
        qry_versiones = reporte.versiones.values(
            'version', 'fecha').all().order_by('-fecha')
        qry_incidentes = reporte.incidentes.values('codigo')
        info_reporte = {
            'reporte': reporte.nombre,
            'id': reporte.id,
            'aplicacion': reporte.aplicacion.nombre,
            'versiones': dict(qry_versiones),
            'incidentes': dict(qry_incidentes)}

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
                mensaje = 'El nuevo nombre del reporte "{}" es: {}'.format(nombre_antiguo, nuevo_nombre)
                return JsonResponse({'ok': mensaje}, status=200)
            else:
                return JsonResponse(
                    {'error': 'No existe el reporte: {}'.format(nombre_antiguo)}, status=400)
        else:
            return JsonResponse(
                {'error': 'Ya existe un reporte con el mismo nombre'}, status=400)


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
class HorariosSoporteView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Vista para consultar los horarios de soporte por Empresa.
    """
    login_url = 'usuarios:login'
    template_name = 'administracion/horarios_soporte.html'

    def test_func(self):
        return self.request.user.usuariosgrexco.tipo == 'A'


class CrearHorariosSoporte(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Vista para consultar los horarios de soporte por Empresa.
    """
    login_url = 'usuarios:login'

    def test_func(self):
        return self.request.user.usuariosgrexco.tipo == 'A'

    def post(self, request, *args, **kwargs):
        data = dict(request.POST)
        nit_empresa = data['selEmpresa'][0]
        horarios = []

        # Recorre el diccionario con los datos de los horarios
        # y crea una lista Modelos creados con estos datos.
        if Empresas.objects.filter(nit=nit_empresa):
            empresa = Empresas.objects.get(nit=nit_empresa)
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
                            inicio=time(hour=hora_inicio[0], minute=hora_inicio[1]),
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
                    return JsonResponse(
                        {'error': 'Los datos no son validos'}, status=400)
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
        qry_empresas = Empresas.objects.filter(
            tiempos_respuesta__empresa__isnull=False).values('nit', 'nombre').distinct()
        empresas = []
        for empresa in qry_empresas:
            empresas.append(empresa)

        return JsonResponse({'empresas': empresas}, status=200)


class CrearTiemposRespuestaView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
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

        # Verifica que la emprea exista
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


# *****************************************************************************
# *                             Dahsboard                                     *
# *****************************************************************************
class DashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """docstring for DashboardView"""
    login_url = 'usuarios:login'
    template_name = 'administracion/dashboard.html'

    def test_func(self):
        return self.request.user.usuariosgrexco.tipo == 'A'


class CreateUserView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
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

        user = User.objects.filter(username=data['nombre_usuario'][0])
        print(user)
        if len(user) != 0:
            return JsonResponse(
                {"error": "El nombre de usuario ya existe"},
                status=400,
            )

        tipo_usuario = data['tipo_usuario'][0]
        if tipo_usuario == 'cliente':
            try:
                user = User.objects.create_user(
                    username=data['nombre_usuario'][0],
                    password='123456',
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



class CompaniesView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Vista consultar empresas
    """
    login_url = 'usuarios:login'
    template_name = 'administracion/companies.html'

    def test_func(self):
        return self.request.user.usuariosgrexco.tipo == 'A'

    def get_context_data(self, *args, **kwargs):
        empresas = Empresas.objects.all()
        plataformas = Plataformas.objects.all()
        aplicaciones = Aplicaciones.objects.all()

        return {'empresas': empresas,
                'plataformas': plataformas,
                'aplicaciones': aplicaciones}


class CreateCompanyView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Vista para crear empresas:
    Orden:
        1. Crear la plataforma.
        2. Crear la empresa.
    """
    login_url = 'usuarios:login'

    def test_func(self):
        return self.request.user.usuariosgrexco.tipo == 'A'

    def post(self, request, *args, **kwargs):
        data = dict(request.POST)

        for k, v in data.items():
            if len(data[k][0]) == 0:
                mensaje = 'El campo {} esta vacio'.format(k.capitalize())
                return JsonResponse(
                    {'error': mensaje}, status=400
                )
                break

        aplicaciones = data['aplicaciones[]']
        plataforma = Plataformas.objects.get(id=int(data['plataforma'][0]))
        empresa = Empresas(
            nit=data['nit'][0],
            nombre=data['nombre'][0],
            direccion=data['direccion'][0],
            telefono=data['telefono'][0],
            plataformas_nombre=plataforma
        )

        try:
            empresa.save()

            for a in aplicaciones:
                app = Aplicaciones.objects.get(id=int(a))
                convenio = Convenios()
                convenio.aplicaciones_id = app
                convenio.empresas_nit = empresa
                convenio.save()

            return JsonResponse({"ok": "Los datos de guardaron correctamente."})
        except Exception as e:
            return JsonResponse({"error": e}, status=400)


class BasicListCompanyView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Retorna un listado con los datos basicos de las Empresas.
    """
    login_url = 'usuarios:login'

    def test_func(self):
        return self.request.user.usuariosgrexco.tipo == 'A'

    def get(self, request, *args, **kwargs):
        qry_empresas = Empresas.objects.values(
            'nit',
            'nombre',
            'direccion',
            'telefono',
            'plataforma__nombre').all()

        empresas = []
        for empresa in qry_empresas:
            empresas.append(empresa)

        return JsonResponse({'empresas': empresas}, status=200)
