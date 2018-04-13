from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Plataformas(models.Model):
    nombre = models.CharField(max_length=30, null=False, blank=False)
    version = models.CharField(max_length=20, null=False, blank=False)

    def __str__(self):
        return " {}:{} ".format(self.nombre, self.version)


class Empresas(models.Model):
    nit = models.CharField(max_length=10, primary_key=True)
    nombre = models.CharField(max_length=100, blank=False, null=False)
    direccion = models.CharField(max_length=150, blank=False, null=False)
    telefono = models.CharField(max_length=12, null=False)
    plataformas_nombre = models.ForeignKey(Plataformas, on_delete=models.CASCADE)

    def __str__(self):
        return 'Empresa: %s' % (self.nombre)


class UsuariosGrexco(models.Model):
    """
    Este modelo extiende los datos del modelo User.
    Se crea para poder restringir el acceso a las vistas dependiendo
    del tipo de usuario que este loggeado.
    Se usa un OneToOneField para crear una relación entre el tipo de usuario
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
    es_coordinador = models.BooleanField(default=False)
    telefono = models.CharField(max_length=15, default=0)
    extension = models.IntegerField(default=0)
    cargo = models.CharField(max_length=30)
    empresas_nit = models.ForeignKey(Empresas, on_delete=models.CASCADE)

    def __str__(self):
        return "usuario: {user_id}, tipo: {tipo}".format(
            user_id=self.user_id.username,
            tipo=self.tipo
        )


class PrioridadesRespuesta(models.Model):
    codigo = models.CharField(max_length=2, primary_key=True)
    descripcion = models.CharField(max_length=20)

    def __str__(self):
        return self.descripcion


class TiemposRespuesta(models.Model):
    empresa = models.ForeignKey('Empresas', on_delete=models.CASCADE)
    prioridades_respuesta = models.ForeignKey(
        'PrioridadesRespuesta',
        on_delete=models.CASCADE,
    )
    tiempo_horas = models.IntegerField(null=True)

    def __str__(self):
        return "Prioridad: {}, tiempo: {} horas".format(
            self.prioridades_respuesta_codigo,
            self.tiempo_horas,
        )


class HorariosSoporte(models.Model):
    """
    Cuando se cree en los parametros para las empresas a las que se presta
    soporte 24Horas va a colocar en los campos 'inicio' y 'fin' = 'null'.
    Y para las empresas que no se preste servicio algun dia de la semana
    sera null en los mismos campos para el dia en cuestion.
    """
    DIAS = (
        ('L', 'Lunes'),
        ('M', 'Martes'),
        ('MI', 'Miercoles'),
        ('J', 'Jueves'),
        ('V', 'Viernes'),
        ('S', 'Sabado'),
        ('D', 'Domingo')
    )

    dia = models.IntegerField()
    empresa = models.ForeignKey('Empresas', on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=2, null=False, choices=DIAS)
    inicio = models.IntegerField(null=True)
    fin = models.IntegerField(null=True)


class Aplicaciones(models.Model):
    nombre = models.CharField(max_length=30,
                              blank=False,
                              unique=True,
                              null=False)

    def __str__(self):
        return '{}'.format(self.nombre)


class Reportes(models.Model):
    nombre = models.CharField(max_length=40, blank=False)
    aplicaciones_id = models.ForeignKey(Aplicaciones,
                                        on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Convenios(models.Model):
    aplicaciones_id = models.ForeignKey(Aplicaciones, on_delete=models.CASCADE)
    empresas_nit = models.ForeignKey(Empresas, on_delete=models.CASCADE)

    def __str__(self):
        return "Empresa: {}, Aplicacion: {}".format(
            self.empresas_nit.nombre,
            self.aplicaciones_id.nombre
        )
