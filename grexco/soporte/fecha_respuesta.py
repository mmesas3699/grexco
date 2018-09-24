"""docstring."""
from datetime import datetime, timedelta

from django.shortcuts import get_object_or_404

from administracion.models import HorariosSoporte
from administracion.models import PrioridadesRespuesta
from administracion.models import TiemposRespuesta

def mas_un_dia(fecha):
    """Recibe una fecha y le agrega un día"""
    un_dia = timedelta(days=1)
    return fecha + un_dia


def verifica_servicio(empresa, fecha_incidente):
    """Retorna un objeto HorariosSoporte."""
    dia = fecha_incidente.weekday()

    return get_object_or_404(HorariosSoporte, empresa=empresa, dia=dia)


def fecha_respuesta(fecha_incidente, tiempo_respuesta, empresa):
    """Calcula la fecha de respuesta para el caso deacuerdo a la prioridad
    asignada."""
    empresa = empresa
    fecha_incidente = fecha_incidente
    tiempo_respuesta = tiempo_respuesta
    horario_soporte = verifica_servicio(empresa, fecha_incidente)

    if horario_soporte.inicio:
        # Se crean las variables 'inicio_soporte' y 'fin_soporte'
        # con los datos 'date' de la fecha del incidente
        inicio_soporte = datetime(
            year=fecha_incidente.year,
            month=fecha_incidente.month,
            day=fecha_incidente.day,
            hour=horario_soporte.inicio.hour,
            minute=horario_soporte.inicio.minute)
        fin_soporte = datetime(
            year=fecha_incidente.year,
            month=fecha_incidente.month,
            day=fecha_incidente.day,
            hour=horario_soporte.fin.hour,
            minute=horario_soporte.fin.minute)
        
        if fecha_incidente < inicio_soporte:
            respuesta = fecha_incidente + tiempo_respuesta
        else:
            respuesta = fecha_incidente + tiempo_respuesta

        if respuesta < fin_soporte:
            print('Guardar', respuesta)
        else:
            tiempo_respuesta = tiempo_respuesta - (fin_soporte - respuesta)
            fecha_respuesta(fecha_incidente, tiempo_respuesta, empresa)
    else:
        fecha_incidente = mas_un_dia(fecha_incidente)
        fecha_respuesta(fecha_incidente, tiempo_respuesta, empresa)