# Generated by Django 2.0.1 on 2018-06-25 11:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incidentes',
            name='tipo_incidente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='incidentes', to='administracion.TiposIncidentes'),
        ),
        migrations.DeleteModel(
            name='TiposIncidentes',
        ),
    ]
