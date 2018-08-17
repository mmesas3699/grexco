"""docstring."""
import datetime

from administracion.models import (
    Empresas, HorariosSoporte, PrioridadesRespuesta, TiemposRespuesta)
from usuarios.models import Incidentes


def verifica_servicio(empresa, dia):
    """
    Verifica si para el dia en cuestión la empresa tiene servicio.

    parametros:
        :empresa    :la empresa que se desea consultar
        :dia        :el dia que se desea verificar
    """
    hs = HorariosSoporte.objects.get(empresa=empresa, dia=dia)
    if hs.inicio:
        return {'incio': hs.inicio, 'fin': hs.fin}
    else:
        return None


def fecha_respuesta(incidente, codigo_prioridad):
    """docstring."""
    incidente = incidente
    empresa = incidente.usuario.usuariosgrexco.empresa
    prioridad = PrioridadesRespuesta.objects.get(codigo=codigo_prioridad)

    # Consulta el tiempo de respuesta para la prioridad
    qry_tiempo_respuesta = TiemposRespuesta.objects.get(
        empresa=incidente.usuario.empresa,
        prioridad=prioridad
    )
    tiempo_respuesta = qry_tiempo_respuesta.tiempo
    tiempo_rta = datetime.timedelta(hours=tiempo_respuesta)

    hora_caso = incidente.fecha_creacion
    hora_respuesta = hora_caso + tiempo_rta
    dia_rta = datetime.date.today()

    servicio = verifica_servicio(empresa, dia_rta.weekday())
    if servicio:
        hora_fin_servicio = datetime.datetime(
            year=dia_rta.year,
            month=dia_rta.month,
            day=dia_rta.day,
            hour=servicio.fin.hour,
            minute=servicio.fin.minute,
            second=00
        )
    else:
    un_dia = datetime.timedelta(days=1)
print(hora_respuesta > hora_fin_servicio)

tiempo_acumulado = hora_fin_servicio - hora_caso
print("tiempo_acumulado:", tiempo_acumulado)

tiempo_rta = tiempo_rta - tiempo_acumulado
print("tiempo_rta:", tiempo_rta)

dia_rta = dia_rta + un_dia
print("dia_rta:", dia_rta)

hora_inicio_servicio = datetime.datetime(
    year=dia_rta.year,
    month=dia_rta.month,
    day=dia_rta.day,
    hour=8,
    minute=00,
    second=00
)
print("hora_inicio_servicio:", hora_inicio_servicio)

hora_respuesta = hora_inicio_servicio + tiempo_rta
print("hora_respuesta:", hora_respuesta)

hora_fin_servicio = datetime.datetime(
    year=dia_rta.year,
    month=dia_rta.month,
    day=dia_rta.day,
    hour=18,
    minute=00,
    second=00
)
print("hora_fin_servicio:", hora_fin_servicio)

print(hora_respuesta > hora_fin_servicio)

fecha_respuesta(hora_caso)
