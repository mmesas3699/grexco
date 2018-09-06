"""docstring."""
import datetime

from administracion.models import HorariosSoporte
from administracion.models import PrioridadesRespuesta
from administracion.models import TiemposRespuesta


def verifica_servicio(empresa, dia):
    """
    Verifica si para el dia en cuestión la empresa tiene servicio.

    parametros:
        :empresa    :la empresa que se desea consultar
        :dia        :el dia que se desea verificar
    """
    hs = HorariosSoporte.objects.get(empresa=empresa, dia=dia)
    if hs.inicio:
        return True
    else:
        return False


def mas_un_dia(fecha):
    """Función que agrega 1 día a la fecha de respuesta."""
    un_dia = datetime.timedelta(days=1)
    fecha_respuesta = fecha + un_dia

    return fecha_respuesta


def inicio_fin_servicio(empresa, dia):
    """Retorna los horarios de inicio y fin servicio para el dia."""
    hs = HorariosSoporte.objects.get(empresa=empresa, dia=dia)
    if hs.inicio:
        return hs
    else:
        return False


def respuesta(incidente, tiempo_respuesta, fecha_respuesta):
    """
    Función para generar la fecha de respuesta de los incidentes.

    Recibe como parametros:

    :incidente           :clase usuarios.models.Incidentes
    :tiempo_respuesta    :clase datetime.timedelta
    :fecha_respuesta     :clase datetime.datetime
    """
    incidente = incidente
    empresa = incidente.usuario.usuariosgrexco.empresa
    fecha_incidente = incidente.fecha_creacion
    print('i', fecha_incidente)
    tiempo_respuesta = tiempo_respuesta
    print('t', tiempo_respuesta)
    fecha_respuesta = fecha_respuesta
    print('r', fecha_respuesta)
    servicio = verifica_servicio(empresa, fecha_respuesta.weekday())
    print('s', servicio)

    while servicio is False:
        fecha_respuesta = mas_un_dia(fecha_respuesta)
        print('w r', fecha_respuesta)
        servicio = verifica_servicio(empresa, fecha_respuesta.weekday())
        print('ser', servicio)

    # Horarios de servicio para la fecha de respuesta
    horario_servicio = inicio_fin_servicio(empresa, fecha_respuesta.weekday())
    print('h s', horario_servicio)

    # Si el mismo dia del caso hay servicio
    if fecha_incidente.date() == fecha_respuesta.date():
        print('mismo dia')
        fecha_respuesta = fecha_incidente + tiempo_respuesta
        print('fr 1', fecha_respuesta)
        f_fin_servicio = datetime.datetime(
            fecha_incidente.year,
            fecha_incidente.month, 
            fecha_incidente.day,
            horario_servicio.fin.hour,
            horario_servicio.fin.minute,
        )
        print('fin serv', f_fin_servicio)
        if fecha_respuesta < f_fin_servicio:
            # return
            fecha_respuesta = fecha_respuesta
            print('1', fecha_respuesta)
        else:
            f_fin_servicio = datetime.datetime(
                fecha_respuesta.year, 
                fecha_respuesta.month, 
                fecha_respuesta.day,
                horario_servicio.fin.hour,
                horario_servicio.fin.minute,
            )
            print('fin serv 1', f_fin_servicio)
            # Calcula el tiempo de respuesta restante
            tiempo_respuesta = fecha_respuesta - f_fin_servicio
            fecha_respuesta = mas_un_dia(fecha_respuesta)
            respuesta(incidente, tiempo_respuesta, fecha_respuesta)
    else:
    # El mismo dia del caso NO hay servicio
        print('dif dia')
        fecha_respuesta = datetime.datetime(
            fecha_respuesta.year, 
            fecha_respuesta.month, 
            fecha_respuesta.day,
            horario_servicio.inicio.hour,
            horario_servicio.inicio.minute,
        ) + tiempo_respuesta
        hora_respuesta = fecha_respuesta.time()
        if hora_respuesta < horario_servicio.fin:
            # return fecha_respuesta
            fecha_respuesta = fecha_respuesta
            print('2', fecha_respuesta)
            return fecha_respuesta
        else:
            f_fin_servicio = datetime.datetime(
                fecha_respuesta.year, 
                fecha_respuesta.month, 
                fecha_respuesta.day,
                horario_servicio.fin.hour,
                horario_servicio.fin.minute,
            )
            print('fin serv 2', f_fin_servicio)
            tiempo_respuesta = fecha_respuesta - f_fin_servicio
            fecha_respuesta = mas_un_dia(fecha_respuesta)
            respuesta(incidente, tiempo_respuesta, fecha_respuesta)
