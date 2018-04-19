"""
Script inicial para crear:

    - Usuario administrador
    - Empresa que presta el servicio
    - Plataforma que usa esta empresa
"""
from django.contrib.auth.models import User

from administracion.models import UsuariosGrexco, Empresas, Plataformas

# Escriba (en mayusculas) el nombre de la plataforma y su version.
nombre_plataforma = 'SQL SERVER'
version_plataforma = '2016'

plataforma = Plataformas(
    nombre=nombre_plataforma,
    version=version_plataforma,
)


def crear_plataforma():
    plataforma.save()


pla = Plataformas.objects.get(nombre=plataforma.nombre)


def crear_empresa(pla):
    # Escriba los datos de su Empresa
    empresa_nit = '8000497311'
    empresa_nombre = 'GREXCO S.A.S'
    empresa_direccion = 'Calle 60a # 5 - 54'
    empresa_telefono = '2351180'

    empresa = Empresas(
        nit=empresa_nit,
        nombre=empresa_nombre,
        direccion=empresa_direccion,
        telefono=empresa_telefono,
        plataforma=pla,
    )

    empresa.save()


# Escriba los datos de su usuario administrador

NOMBRE_USUARIO = 'adms'  # Es el usuario que va a usar en la plataforma: Ej: 'admin'
CONTRASEÑA = 'grexco02'
nombre_responsable = 'Miguel'  # El primer nombre del responsable de usar este usuario
apellido_responsable = 'Mesa'  # El apellido del responsable de usar este usuario
email_responsable = 'miguel.mesa@grexco.com.co'
telefono_responsable = '2351180'
extension = 123  # Numerico
cargo_responsable = 'Consultor Funcional'

usr = User.objects.create_user(
    username=NOMBRE_USUARIO,
    password=CONTRASEÑA,
    first_name=nombre_responsable,
    last_name=apellido_responsable,
    email=email_responsable,
)

adms = UsuariosGrexco(
    usuario=usr,
    tipo='A',
    es_coordinador=True,
    telefono=telefono_responsable,
    extension=extension,
    cargo=cargo_responsable,
    empresa=empresa,
)


adms.save()

crear_empresa(pla)
