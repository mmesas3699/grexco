# Generated by Django 2.0.1 on 2018-07-05 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0009_auto_20180704_1218'),
    ]

    operations = [
        migrations.CreateModel(
            name='MovimientosEstadosIncidentes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='estado', to='usuarios.EstadosIncidentes')),
                ('incidente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='incidente', to='usuarios.Incidentes')),
            ],
        ),
    ]
