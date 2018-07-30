"""Modelos para la aplicación de Soporte."""

from django.contrib.auth.models import User
from django.db import models

from administracion.models import ubicacion_archivos
from usuarios.models import Incidentes
from tecnologia.models import Cambios


# Create your models here.


class ResultadosPruebas(models.Model):
    codigo = models.CharField(primary_key=True, max_length=1)
    descripcion = models.CharField(max_length=20)

    def __str__(self):
        return '{}'.format(self.descripcion)


class Pruebas(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    cambio = models.ForeignKey(
        Cambios, on_delete=models.PROTECT, related_name='pruebas')
    fecha = models.DateTimeField(auto_now_add=True)
    resultado = models.ForeignKey(
        ResultadosPruebas, on_delete=models.PROTECT, related_name='pruebas')

    def __str__(self):
        return '{}:{}'.format(self.id, self.resultado)


class ArchivosPruebas(models.Model):
    prueba = models.ForeignKey(
        Pruebas, on_delete=models.PROTECT, related_name='adjuntos')
    archivo = models.FileField(
        storage=ubicacion_archivos, upload_to='pruebas/{}'.format(prueba))

    def __str__(self):
        return '{}'.format(self.archivo)


class NotasSoporte(models.Model):
    incidente = models.ForeignKey(
        Incidentes, on_delete=models.PROTECT)
    usuario = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='usuario_soporte')
    fecha = models.DateTimeField(auto_now_add=True)
    nota = models.TextField(null=True, blank=True)


class NotasTecnologia(models.Model):
    incidente = models.ForeignKey(
        Incidentes, on_delete=models.PROTECT)
    usuario = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='usuario_tecnologia')
    fecha = models.DateTimeField(auto_now_add=True)
    nota = models.TextField(null=True, blank=True)
