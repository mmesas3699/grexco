import datetime

from usuarios.models import Incidentes

from soporte.fecha_respuesta import fecha_respuesta


incidente = Incidentes.objects.get(codigo=2)
fecha = incidente.fecha_creacion
tiempo = datetime.timedelta(hours=16)
emp = incidente.usuario.usuariosgrexco.empresa

r = fecha_respuesta(fecha, tiempo, emp)
print('resp', r)