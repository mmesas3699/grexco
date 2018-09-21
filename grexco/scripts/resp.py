import datetime

from usuarios.models import Incidentes

from soporte.fecha_respuesta import respuesta


incidente = Incidentes.objects.get(codigo=2)
fecha = incidente.fecha_creacion
tiempo = datetime.timedelta(hours=16)

r = respuesta(incidente, tiempo, fecha)
print('resp', r)