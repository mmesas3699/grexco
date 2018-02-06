from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns

# Create your models here.

class Contact(models.Model):
    """
    Modelo del formulario de contacto
    """
    id = models.AutoField(db_column='Id', primary_key=True)
    nombre = models.CharField(db_column='Nom', max_length=50, null=False)
    telefono = models.BigIntegerField(db_column='Tel', null=False)
    empresa = models.CharField(db_column='Emp', max_length=100, null=False)
    email = models.EmailField(db_column='Email')
    mensaje = models.CharField(db_column='Msj', max_length=2000, null=False)
    fecha = models.DateTimeField(auto_now=True)

    def __str__(self):
    	return self.nombre

    def get_absolute_url(self):
        """
        Retorna la url para acceder a un mensaje en particular
        """
        return reverse('detalle-del-mensaje', args=[str(self.id)])
