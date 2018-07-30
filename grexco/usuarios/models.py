"""Se definen los models de la aplicación Usuarios."""
from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
import administracion.models as administracion

# Create your models here.

ubicacion_archivos = FileSystemStorage(
    location='/mnt/c/Users/arju/Desktop/Grexco/Proyectos/Web/grexco/usuarios/')


def my_awesome_upload_function(instance, filename):
    """Esta función retorn la ruta para guardar los archivos."""
    return 'incidentes/' + instance.incidente.codigo + '/' + 'adjuntos/' + filename


class EstadosIncidentes(models.Model):
    """
    Se definen los diferentes estados que tendran los incidentes.

        C = Creado (Cuando el cliente crea el incidente)
        S = Soporte (Cuando el caso es asignado a un integrante de soporte)
        T = Tecnología (Cuando soporte envia el caso a Tecnología)
        P = Pruebas (Cuando tecnologia lo devuelve a soporte)
        E = Entregado (Cuando soporte envia la respuesta al cliente)
        So = Solucionado (Cuando el cliente cierra el caso)
    """

    codigo = models.CharField(primary_key=True, max_length=3)
    descripcion = models.CharField(max_length=20)

    def __str__(self):
        """docstring."""
        return '{}:{}'.format(self.codigo, self.descripcion)


class Incidentes(models.Model):
    codigo = models.PositiveIntegerField(primary_key=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    titulo = models.CharField(max_length=80)
    descripcion = models.TextField()
    usuario = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='incidentes'
    )
    tipo_incidente = models.ForeignKey(
        administracion.TiposIncidentes,
        on_delete=models.PROTECT,
        related_name='incidentes',
        blank=True,
        null=True
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
        related_name='incidentes',
        blank=True,
        null=True
    )
    estado = models.ForeignKey(
        EstadosIncidentes,
        on_delete=models.PROTECT,
        related_name='incidentes'
    )
    fecha_respuesta = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        """docstring."""
        return 'codigo: {}'.format(self.codigo)


class Adjuntos(models.Model):
    incidente = models.ForeignKey(
        Incidentes, on_delete=models.CASCADE, related_name='adjuntos', default=0)
    nombre_archivo = models.CharField(max_length=250, blank=True, null=True)
    archivo = models.FileField(
        storage=ubicacion_archivos,
        upload_to=my_awesome_upload_function)

    def __str__(self):
        return 'incidente:{}, archivo:{}'.format(self.incidente, self.archivo)


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
        User,
        on_delete=models.CASCADE,
        related_name='incidentes_soporte'
    )
    incidente = models.ForeignKey(
        Incidentes, on_delete=models.PROTECT, related_name='usuarios_soporte')

    def __str__(self):
        return '{}:{}'.format(self.usuario, self.incidente)


class UsuariosTecnologiaIncidentes(models.Model):
    usuario = models.ForeignKey(
        administracion.UsuariosGrexco,
        on_delete=models.CASCADE,
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
        User,
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
        on_delete=models.CASCADE,
        related_name='adjuntos'
    )
    archivo = models.FileField(
        storage=administracion.ubicacion_archivos,
        upload_to='incidentes/respuestas/{}'.format(respuesta)
    )

    def __str__(self):
        return '{}'.format(self.respuesta)
