from django.http import JsonResponse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User

from administracion.models import (UsuariosGrexco,
                                   Empresas,
                                   Plataformas,
                                   Aplicaciones,
                                   Convenios)


# Create your views here.

class LoginView(TemplateView):
    """docstring for LoginView"""
    template_name = 'administracion/login.html'


class DashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """docstring for DashboardView"""
    login_url = 'usuarios:login'
    template_name = 'administracion/dashboard.html'

    def test_func(self):
        return self.request.user.usuariosgrexco.tipo == 'A'


class CreateUserView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    El orden para crear un usuario:
        1. Plataforma
        2. Empresa
        3. User
        4. UsuariosGrexco
    """
    login_url = 'usuarios:login'
    template_name = 'administracion/nuevo_usuario.html'

    def test_func(self):
        return self.request.user.usuariosgrexco.tipo == 'A'

    def get_context_data(self):
        empresas = Empresas.objects.all()

        return {'empresas': empresas}

    def post(self, request, *args, **kwargs):
        body = dict(request.POST)

        user = User.objects.filter(username=body['username'][0])

        if user:
            return JsonResponse({"error": "El nombre del usuario ya existe"})
        else:
            return JsonResponse({"ok": "El nombre esta disponible"})


class PlatformView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    """
    Vista para consultar plataformas
    """
    login_url = 'usuarios:login'
    template_name = 'administracion/platforms.html'

    def test_func(self):
        return self.request.user.usuariosgrexco.tipo == 'A'

    def get_context_data(self, *args, **kwargs):
        plataforma = Plataformas.objects.all()

        return {'plataformas': plataforma}


class CreatePlatformView(LoginRequiredMixin,
                         UserPassesTestMixin,
                         TemplateView):
    """
    Vista para crear plataformas
    """
    login_url = 'usuarios:login'
    template_name = 'administracion/new_platform.html'

    def test_func(self):
        return self.request.user.usuariosgrexco.tipo == 'A'

    def post(self, request, *args, **kwargs):
        data = dict(request.POST)
        name = data['name'][0]
        version = data['plt-version'][0]

        if len(name) == 0 or len(version) == 0:
            return JsonResponse(
                {"error": "Los campos estan vacios"},
                status=400
            )

        plataforma = Plataformas.objects.filter(nombre=name, version=version)

        # Punto de control
        # print(plataforma)

        if plataforma.exists():
            return JsonResponse({"error": "Los datos ya existen"}, status=400)
        else:
            plt = Plataformas()
            plt.nombre = name
            plt.version = version

            try:
                plt.save()
                return JsonResponse({"ok": "ok"})
            except Exception as e:
                return JsonResponse(
                    {"error": "Ocurrio un error al grabar los datos"},
                    status=400
                )


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

        print(data)
        aplicaciones = data['aplicaciones[]']
        plataforma = Plataformas.objects.get(id=int(data['plataforma'][0]))
        empresa = Empresas(
            nit=data['nit'][0],
            nombre=data['nombre'][0],
            direccion=data['direccion'][0],
            telefono=data['telefono'][0],
            plataformas_nombre=plataforma
        )
        """
        try:
            empresa.save()

            for a in aplicaciones:
                app = Aplicaciones.objects.get(id=int(a))
                convenio = Convenios()
                convenio.aplicaciones_id = app
                convenio.empresas_nit = empresa
                convenio.save()

            return JsonResponse(
                {"ok": "Los datos de guardaron correctamente."}
            )
        except Exception as e:
            return JsonResponse(
                {"error": e},
                status=400
            )
        """
