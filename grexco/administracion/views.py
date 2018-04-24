from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.contrib.auth.models import User
import pyexcel as pe


from administracion.models import (
    UsuariosGrexco,
    Empresas,
    Plataformas,
    Aplicaciones,
    Convenios
)

# Create your views here.

def genera_id(x):
    """
    Recibe como parametro un Queryset de:
    Modelo.objects.last() 
    """
    if x is None:
        return 0
    else:
        return x.id + 1


class LoginView(TemplateView):
    """docstring for LoginView"""
    template_name = 'administracion/login.html'

    def post(self, request):
        data = dict(request.POST)
        # print(data)
        usuario = authenticate(
            request,
            username=data['nombre'][0],
            password=data['contraseña'][0])
        print(usuario)
        if usuario is not None:
            print('ok')
            login(request, usuario)
            # return redirect('administracion:dashboard')
            return JsonResponse({'ok': 'ok'}, status=200)
        else:
            print('error')
            return JsonResponse({'error' : 'Datos invalidos o usuario inactivo'}, status=400)


# ********************
# *   Plataformas    *
# ********************
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


class CreatePlatformView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
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

        if len(nombre) == 0 or len(version) == 0:
            return JsonResponse(
                {"error": "Los campos estan vacios"},
                status=400
            )

        plataforma = Plataformas.objects.filter(
            nombre=nombre.upper(),
            version=version.upper()
        )

        if plataforma.exists():
            return JsonResponse({"error": "Los datos ya existen"}, status=400)
        else:
            id = Plataformas.objects.values('id').last()['id'] + 1
            # print(id)
            plt = Plataformas(id=id, nombre=nombre.upper(), version=version)
            # print(plt)
            try:
                plt.save()
            except Exception as e:
                mensaje = "Ocurrio un error al grabar los datos: {}".format(e)
                return JsonResponse(
                    {"error": mensaje},
                    status=400
                )

            mensaje = "Se guardo la plataforma: {}".format(plt)
            return JsonResponse({"ok": mensaje})


class DeletePlatformView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Vista para eliminar plataformas
    """
    login_url = 'usuarios:login'
    template_name = 'administracion/companies.html'

    def test_func(self):
        return self.request.user.usuariosgrexco.tipo == 'A'

    def post(self, request, *args, **kargs):
        data = dict(request.POST)
        # print(data)
        for k, v in data.items():
            plataforma = Plataformas.objects.get(id=int(data[k][0]))
            if plataforma:
                from django.db.models.deletion import ProtectedError
                # print(plataforma.nombre)
                try:
                    plataforma.delete()
                except ProtectedError as e:
                    empresa = Empresas.objects.get(plataforma__id=plataforma.id)
                    msj = "No es posible eliminar: {}-{}. Pertenece a la empresa: {}".format(
                        plataforma.nombre,
                        plataforma.version,
                        empresa.nombre,
                    )
                    return JsonResponse({'error': msj}, status=400)

        mensaje = 'Se eliminó la plataforma: {}'.format(plataforma.nombre)
        return JsonResponse({'ok': mensaje}, status=200)


# *****************
# *  Aplicaciones *
# *****************
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
            x = Aplicaciones.objects.last()
            id = genera_id(x)
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
                x = Aplicaciones.objects.last()
                id = genera_id(x)
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


# ****************
# *  Dahsboard   *
# ****************
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
