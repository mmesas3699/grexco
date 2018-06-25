"""
Script inicial para crear:

    - Usuario administrador
    - Empresa que presta el servicio
    - Plataforma que usa esta empresa
"""
from django.contrib.auth.models import User
from django.db import transaction

from administracion.models import Empresas
from administracion.models import UsuariosGrexco
from administracion.models import Plataformas
from administracion.models import PrioridadesRespuesta


# *************************************************************
# *              DATOS USUARIO ADMINISTRADOR                  *
# *************************************************************
# El nombre de usuario que va a usar en la aplicación de Administración.
# Ejemplo: 'admin'
NOMBRE_USUARIO = 'adms'

# Elija un contraseña alfa-numerica.
CONTRASEÑA = 'grexco02'

# El primer nombre de la persona responsable de este usuario.
NOMBRE_RESPONSABLE = 'Miguel'

# El apellido de la persona responsbel de este usuario.
APELLIDO_RESPONSABLE = 'Mesa'
EMAIL_RESPONSABLE = 'miguel.mesa@grexco.com.co'
TELEFONO_RESPONSABLE = '2351180'
EXTENSION = 123  # Numerico
CARGO_RESPONSABLE = 'Consultor Funcional'


# *************************************************************
# *      DATOS PLATAFORMA USADA POR SU EMPRESA                *
# *************************************************************
# Escriba (en mayusculas) el nombre de la plataforma y su version.
# Ejemplo: 'SQL SERVER', 2016
NOMBRE_PLATAFORMA = 'SQL SERVER'
VERSION_PLATAFORMA = '2016'


# *************************************************************
# *                    DATOS EMPRESA                          *
# *************************************************************
# Escriba los datos de su Empresa
EMPRESA_NIT = '8000497311'
EMPRESA_NOMBRE = 'GREXCO S.A.S'
EMPRESA_DIRECCION = 'Calle 60a # 5 - 54'
EMPRESA_TELEFONO = '2351180'


# ____________________________________________________________
#                   PRIORIDADES DE RESPUESTA
# ____________________________________________________________
PRIORIDADES = [['a', 'Alta'], ['m', 'Media'], ['b', 'Baja']]

def crear_prioridades():
    with transaction.atomic():
        for p in PRIORIDADES:
            prioridad = PrioridadesRespuesta(codigo=p[0], descripcion=p[1])
            prioridad.save()


if __name__ == '__main__':

    # Instancia la plataforma
    plataforma = Plataformas(id=1, nombre=NOMBRE_PLATAFORMA, version=VERSION_PLATAFORMA)

    # Graba la plataforma
    plataforma.save()

    # Trae el objeto Plataforma
    p = Plataformas.objects.get(nombre=plataforma.nombre)

    # Graba la empresa
    empresa = Empresas(nit=EMPRESA_NIT, nombre=EMPRESA_NOMBRE, direccion=EMPRESA_DIRECCION, telefono=EMPRESA_TELEFONO, plataforma=p)
    empresa.save()

    # Graba los datos basicos del usuario
    usuario = User.objects.create_user(username=NOMBRE_USUARIO, password=CONTRASEÑA, first_name=NOMBRE_RESPONSABLE, last_name=APELLIDO_RESPONSABLE, email=EMAIL_RESPONSABLE)

    # Graba los datos del usuario administrador
    usr = User.objects.get(username=usuario.username)
    usuario_administrador = UsuariosGrexco(usuario=usr, tipo='A', es_coordinador=True, telefono=TELEFONO_RESPONSABLE, extension=EXTENSION, cargo=CARGO_RESPONSABLE, empresa=empresa)
    usuario_administrador.save()
