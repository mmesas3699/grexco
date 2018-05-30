from django.db import models

from administracion.models import ubicacion_archivos
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
