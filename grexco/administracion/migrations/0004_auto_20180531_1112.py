# Generated by Django 2.0.1 on 2018-05-31 11:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0003_auto_20180530_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tiemposrespuesta',
            name='empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tiempos_respuesta', to='administracion.Empresas'),
        ),
    ]
