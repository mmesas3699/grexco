from django.db import models

import administracion.models as administracion

# Create your models here.


class Incidentes(models.Model):
    codigo = models.PositiveIntegerField(primary_key=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField()
    usuario = models.ForeignKey(
        administracion.UsuariosGrexco,
        on_delete=models.PROTECT,
        related_name='incidentes'
    )
    tipo_incidente = models.ForeignKey(
        administracion.TiposIncidentes,
        on_delete=models.PROTECT,
        related_name='incidentes'
    )
    reporte = models.ForeignKey(
        administracion.Reportes,
        on_delete=models.PROTECT,
        related_name='incidentes',
        blank=True,
        null=True
    )
    aplicacion = models.ForeignKey(
        administracion.Aplicaciones,
        on_delete=models.PROTECT,
        related_name='incidentes',
        blank=True,
        null=True
    )
    prioridad_respuesta = models.ForeignKey(
        administracion.PrioridadesRespuesta,
        on_delete=models.PROTECT,
        related_name='incidentes'
    )
    fecha_respuesta = models.DateTimeField()

    def __str__(self):
        return '{}:{}'.format(self.codigo, self.usuario)


class Adjuntos(models.Model):
    incidente = models.ForeignKey(
        Incidentes, on_delete=models.PROTECT, related_name='adjuntos')
    archivo = models.FileField(
        storage=administracion.ubicacion_archivos,
        upload_to='incidentes/{}/'.format(incidente))

    def __str__(self):
        return '{}:{}'.format(self.incidente, self.archivo)


class EstadosIncidentes(models.Model):
    codigo = models.CharField(primary_key=True, max_length=3)
    descripcion = models.CharField(max_length=20)

    def __str__(self):
        return '{}:{}'.format(self.codigo, self.descripcion)


class IncidentesReportes(models.Model):
    incidente = models.ForeignKey(
        Incidentes,
        related_name='incidentes_reportes',
        on_delete=models.PROTECT
    )
    reporte = models.ForeignKey(
        administracion.Reportes,
        related_name='incidentes_reportes',
        on_delete=models.PROTECT
    )

    def __str__(self):
        return "{}:{}".format(self.incidente, self.reporte)


class UsuariosSoporteIncidentes(models.Model):
    usuario = models.ForeignKey(
        administracion.UsuariosGrexco,
        on_delete=models.PROTECT,
        related_name='incidentes_soporte'
    )
    incidente = models.ForeignKey(
        Incidentes, on_delete=models.PROTECT, related_name='usuarios_soporte')

    def __str__(self):
        return '{usuario}:{incidente}'.format(self.usuario, self.incidente)


class UsuariosTecnologiaIncidentes(models.Model):
    usuario = models.ForeignKey(
        administracion.UsuariosGrexco,
        on_delete=models.PROTECT,
        related_name='incidentes_tecnologia'
    )
    incidente = models.ForeignKey(
        Incidentes,
        on_delete=models.PROTECT,
        related_name='usuarios_tecnologia'
    )

    def __str__(self):
        return '{usuario}:{incidente}'.format(self.usuario, self.incidente)


class MovimientosIncidentes(models.Model):
    incidente = models.ForeignKey(
        Incidentes, on_delete=models.PROTECT, related_name='movimientos')
    estado = models.ForeignKey(
        EstadosIncidentes,
        on_delete=models.PROTECT,
        related_name='movimientos'
    )
    responsable = models.ForeignKey(
        administracion.UsuariosGrexco,
        on_delete=models.PROTECT,
        related_name='movimentos_incidentes'
    )
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}:{}:{}'.format(self.estado, self.incidente, self.fecha)


class RespuestasIncidentes(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    incidente = models.ForeignKey(
        Incidentes,
        on_delete=models.PROTECT,
        related_name='respuesta'
    )
    fecha = models.DateTimeField(auto_now_add=True)
    respuesta = models.TextField()

    def __str__(self):
        return '{}:{}'.format(self.id, self.respuesta)


class AdjuntosRespuestasIncidentes(models.Model):
    respuesta = models.ForeignKey(
        RespuestasIncidentes,
        on_delete=models.PROTECT,
        related_name='adjuntos'
    )
    archivo = models.FileField(
        storage=administracion.ubicacion_archivos,
        upload_to='incidentes/respuestas/{}'.format(respuesta)
    )

    def __str__(self):
        return '{}'.format(self.respuesta)
