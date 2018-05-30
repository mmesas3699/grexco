from django.db import models

from administracion.models import Aplicaciones
from administracion.models import Reportes
from administracion.models import UsuariosGrexco
from usuarios.models import Incidentes

# Create your models here.


class TiposCambios(models.Model):
    codigo = models.CharField(max_length=1, primary_key=True)
    descripcion = models.CharField(max_length=20)

    def __str__(self):
        return '{}'.format(self.descripcion)


class EstadosCambios(models.Model):
    codigo = models.CharField(max_length=1, primary_key=True)
    descripcion = models.CharField(max_length=15)

    def __str__(self):
        return '{}'.format(self.descripcion)


class VersionesAplicaciones(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    version = models.CharField(max_length=20, blank=False, null=False)
    commit = models.CharField(max_length=30, blank=False, null=False)
    fecha = models.DateField()
    aplicacion = models.ForeignKey(
        Aplicaciones, related_name='versiones', on_delete=models.PROTECT)

    def __str__(self):
        return "{}:{}".format(self.aplicacion, self.version)


class VersionesReportes(models.Model):
    id = models.PositiveSmallIntegerField(primary_key=True)
    version = models.CharField(max_length=20, blank=False, null=False)
    commit = models.CharField(max_length=30, blank=False, null=False)
    fecha = models.DateField()
    reporte = models.ForeignKey(
        Reportes, related_name='versiones', on_delete=models.PROTECT)

    def __str__(self):
        return "{}:{}".format(self.reporte, self.version)


class Cambios(models.Model):
    codigo = models.PositiveIntegerField(primary_key=True)
    tipo = models.ForeignKey(
        TiposCambios, on_delete=models.PROTECT, related_name='cambios')
    descripcion = models.TextField()
    estado = models.ForeignKey(
        EstadosCambios, on_delete=models.PROTECT, related_name='estados_cambios')
    version_aplicacion = models.ForeignKey(
        VersionesAplicaciones,
        on_delete=models.PROTECT,
        related_name='cambios',
        blank=True,
        null=True
    )
    versiones_reportes = models.ForeignKey(
        VersionesReportes,
        on_delete=models.PROTECT,
        related_name='cambios',
        blank=True,
        null=True
    )
    incidente = models.ForeignKey(
        Incidentes,
        on_delete=models.PROTECT,
        related_name='cambios',
        blank=True,
        null=True
    )
    usuario = models.ForeignKey(
        UsuariosGrexco, on_delete=models.PROTECT, related_name='cambios')
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{},{},{}'.format(self.codigo, self.estado, self.fecha)
