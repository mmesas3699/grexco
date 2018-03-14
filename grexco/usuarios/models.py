from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class TypeUser(models.Model):
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

        user_type = TypeUser(user_id_id=usr.id, user_name=usr.username, ......)
        user_type.save()
    """
    TYPES_OF_USER = (
        ('C', 'Cliente'),
        ('S', 'Soporte'),
        ('T', 'Teconologia'),
        ('A', 'Administrador')
    )

    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=50, null=False)
    type = models.CharField(max_length=1, null=False, choices=TYPES_OF_USER)
    is_chief = models.BooleanField(default=False)
