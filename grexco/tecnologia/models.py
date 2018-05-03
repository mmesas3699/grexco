from django.db import models

from administracion.models import Aplicaciones

# Create your models here.

class VersionesAplicaciones(models.Model):
    id =  models.PositiveSmallIntegerField(primary_key=True)
    version = models.CharField(max_length=20, blank=False, null=False)
    commit = models.CharField(max_length=30, blank=False, null=False)
    fecha = models.DateField()
    aplicacion = models.ForeignKey(Aplicaciones, related_name='versiones', on_delete=models.PROTECT)

    def __str__(self):
        return "{}:{}".format(self.aplicacion, self.version)
