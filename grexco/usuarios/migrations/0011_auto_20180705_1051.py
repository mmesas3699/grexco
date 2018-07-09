# Generated by Django 2.0.1 on 2018-07-05 10:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0012_auto_20180625_1634'),
        ('usuarios', '0010_movimientosestadosincidentes'),
    ]

    operations = [
        migrations.AddField(
            model_name='incidentes',
            name='estado',
            field=models.ForeignKey(default='C', on_delete=django.db.models.deletion.PROTECT, related_name='incidentes', to='usuarios.EstadosIncidentes'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movimientosestadosincidentes',
            name='usuario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='incidente', to='administracion.UsuariosGrexco'),
        ),
    ]
