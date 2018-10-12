import datetime

from usuarios.models import Incidentes
from soporte.fecha_respuesta import respuesta


incidente = Incidentes.objects.get(codigo=1)
fecha_incidente = incidente.fecha_creacion
tiempo = datetime.timedelta(hours=16)
empresa = incidente.usuario.usuariosgrexco.empresa

r = respuesta(fecha_incidente, tiempo, empresa)
print('respuesta', r)
