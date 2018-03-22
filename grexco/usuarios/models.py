from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class TiposUsuarios(models.Model):
    """
    Este modelo extiende los datos del modelo User.
    Se crea para poder restringir el acceso a las vistas dependiendo
    del tipo de usuario que este loggeado.
    Use un OneToOneField para crear una relación entre el tipo de usuario
    y el usuario (User).

    ** Importante
    Cuando se cree un usuario:
        usr = User.objects.create_user(username='', ....)

    Tambien se debe actualizar este modelo con la relacion correspondiente:

        from django.contrib.auth.models import User

        user = User.objects.get(username='mmesas')
        # para el campo que tiene la relacion se debe guardar la instacia
        # del objeto User no User.id
        user_type = TypeUser(user_id=user, user_name=user.username, ......)
        user_type.save()
    """
    TIPOS_DE_USUARIO = (
        ('C', 'Cliente'),
        ('S', 'Soporte'),
        ('T', 'Teconologia'),
        ('A', 'Administrador')
    )

    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=1, null=False, choices=TIPOS_DE_USUARIO)
    is_chief = models.BooleanField(default=False)

    def __str__(self):
        return self.type


class Plataformas(models.Model):
    nombre = models.CharField(max_length=15, null=False, default='plataforma')
    version = models.CharField(max_length=15, null=False)

    def __str__(self):
        return self.nombre


class Empresas(models.Model):
    nit = models.CharField(max_length=10, primary_key=True)
    empresa = models.CharField(max_length=100, blank=False, null=False)
    cod_verificacion = models.IntegerField(null=True, blank=True)
    direccion = models.CharField(max_length=50, blank=False, null=False)
    telefono = models.CharField(max_length=12, null=False)
    plataforma = models.ForeignKey(Plataformas, on_delete=models.CASCADE)

    def __str__(self):
        return 'Empresa: %s' % (self.empresa)


class EmpresasUsuarios(models.Model):
    empresa_nit = models.ForeignKey(Empresas, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return 'Empresa: %s, Usuario: %s' % (self.empresa_nit, self.user_id)
