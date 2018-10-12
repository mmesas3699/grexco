# -*- coding: utf-8 -*-
"""docstring."""
from datetime import datetime
from datetime import timedelta

from administracion.models import HorariosSoporte
from administracion.models import PrioridadesRespuesta
from administracion.models import TiemposRespuesta


def mas_un_dia(fecha, empresa):
    """Agrega un día a la fecha recidida y le asigna el horario correspondiente
    al inicio del servicio para ese día."""
    fecha = fecha
    empresa = empresa
    un_dia = timedelta(days=1)
    nueva_fecha = fecha + un_dia
    h_servicio = servicio(empresa, nueva_fecha)

    if h_servicio:
        print('mas_un_dia', h_servicio)
        fecha_respuesta = datetime(
            year=nueva_fecha.year, month=nueva_fecha.month,
            day=nueva_fecha.day, hour=h_servicio['inicio'].hour,
            minute=h_servicio['inicio'].minute)
        return fecha_respuesta
    else:
        mas_un_dia(nueva_fecha, empresa)


def servicio(empresa, fecha):
    """Verifica si el dia de la semana que se obtiene de la fecha
    entregada por parametro hay servicio, si no agrega un día
    a esa fecha hasta encontrar un dia con servicio.

    Retorna un objeto de la clase HorariosSoporte con los horarios
    par el día obtenido."""
    empresa = empresa
    fecha = fecha
    dia = fecha.weekday()
    horarios_servicio = HorariosSoporte.objects.get(
        empresa=empresa, dia=dia)

    if horarios_servicio.inicio:
        inicio_servicio = datetime(
            year=fecha.year, month=fecha.month, day=fecha.day,
            hour=horarios_servicio.inicio.hour,
            minute=horarios_servicio.inicio.minute)
        fin_servicio = datetime(
            year=fecha.year, month=fecha.month, day=fecha.day,
            hour=horarios_servicio.fin.hour,
            minute=horarios_servicio.fin.minute)
        return {'inicio': inicio_servicio, 'fin': fin_servicio}
    else:
        return None


def respuesta(fecha_incidente, tiempo_respuesta, empresa):
    fecha_incidente = fecha_incidente
    print('fecha incidente:', fecha_incidente)
    tiempo_respuesta = tiempo_respuesta
    print('tiempo respuesta', tiempo_respuesta)
    empresa = empresa
    
    # Contiene los horaris de servicio
    horario_servicio = servicio(empresa, fecha_incidente)
    
    # Verifica si hay servicio, si No hay entonces agrega un dia
    # a la fecha actual.
    if horario_servicio:
        print('si hay servicio', horario_servicio)
        if fecha_incidente >= horario_servicio['inicio'] and \
                fecha_incidente <= horario_servicio['fin']:
            print('esta entre los horarios de soporte')
            fecha_respuesta = fecha_incidente + tiempo_respuesta

            # Verifica si la fecha de la respuesta es mayor que la fecha fin
            # del servicio.
            if fecha_respuesta < horario_servicio['fin']:
                # Si es menor se calcula la fecha de respuesta
                print('si es menor')
                return "si es menor"
            else:
                # Si es mayor se suma un dia y se realizar el proceso nuevamente.
                # Tiempo de respuesta restante
                tiempo_respuesta = (
                    tiempo_respuesta - (horario_servicio['fin'] - fecha_incidente))
                # Más un dia
                fecha_respuesta = mas_un_dia(fecha_incidente, empresa)
                # Calcula la fecha nuevamente
                respuesta(fecha_respuesta, tiempo_respuesta, empresa)
        else:
            print('2')
            fecha_respuesta = mas_un_dia(fecha_incidente, empresa)
            print('2 - ', fecha_respuesta)
            respuesta(fecha_respuesta, tiempo_respuesta, empresa)
    else:
        fecha_respuesta = mas_un_dia(fecha_incidente, empresa)
        respuesta(fecha_respuesta, tiempo_respuesta, empresa)

    return fecha_respuesta
