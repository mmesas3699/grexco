
fecha_respuesta(hora_caso)


import datetime

un_dia = datetime.timedelta(days=1)
hora_caso = datetime.datetime.now()
tiempo_rta = datetime.timedelta(hours=6)
hora_respuesta = hora_caso + tiempo_rta
dia_rta = datetime.date.today()
hora_fin_servicio = datetime.datetime(
    year=dia_rta.year,
    month=dia_rta.month,
    day=dia_rta.day,
    hour=18,
    minute=00,
    second=00
)

print("hora_caso:", hora_caso)
print("tiempo_rta:", tiempo_rta)
print("hora_respuesta:", hora_respuesta)
print("dia_rta:", dia_rta)
print("hora_fin_servicio:", hora_fin_servicio)

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

def fecha_respuesta(hora_caso):
	
	pass