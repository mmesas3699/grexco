import datetime

hora_caso = datetime.datetime.now()


def fecha_respuesta(fecha_caso):
    hora_caso = fecha_caso
    un_dia = datetime.timedelta(days=1)
    print(hora_caso)


fecha_respuesta(hora_caso)
