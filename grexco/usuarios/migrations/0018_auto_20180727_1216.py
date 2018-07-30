# Generated by Django 2.0.1 on 2018-07-27 12:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0017_auto_20180727_1207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adjuntosrespuestasincidentes',
            name='respuesta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='adjuntos', to='usuarios.RespuestasIncidentes'),
        ),
        migrations.AlterField(
            model_name='usuariostecnologiaincidentes',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='incidentes_tecnologia', to='administracion.UsuariosGrexco'),
        ),
    ]
