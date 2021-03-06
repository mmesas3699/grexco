# Generated by Django 2.0.1 on 2018-05-29 14:15

import django.core.files.storage
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('administracion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Adjuntos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', models.FileField(storage=django.core.files.storage.FileSystemStorage(location='/home/grexco'), upload_to='incidentes/<django.db.models.fields.related.ForeignKey>/')),
            ],
        ),
        migrations.CreateModel(
            name='AdjuntosRespuestasIncidentes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', models.FileField(storage=django.core.files.storage.FileSystemStorage(location='/home/grexco'), upload_to='incidentes/respuestas/<django.db.models.fields.related.ForeignKey>')),
            ],
        ),
        migrations.CreateModel(
            name='EstadosIncidentes',
            fields=[
                ('codigo', models.CharField(max_length=3, primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Incidentes',
            fields=[
                ('codigo', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('descripcion', models.TextField()),
                ('fecha_respuesta', models.DateTimeField()),
                ('aplicacion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='incidentes', to='administracion.Aplicaciones')),
                ('prioridad_respuesta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='incidentes', to='administracion.PrioridadesRespuesta')),
                ('reporte', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='incidentes', to='administracion.Reportes')),
            ],
        ),
        migrations.CreateModel(
            name='IncidentesReportes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('incidente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='incidentes_reportes', to='usuarios.Incidentes')),
                ('reporte', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='incidentes_reportes', to='administracion.Reportes')),
            ],
        ),
        migrations.CreateModel(
            name='MovimientosIncidentes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='movimientos', to='usuarios.EstadosIncidentes')),
                ('incidente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='movimientos', to='usuarios.Incidentes')),
                ('responsable', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='movimentos_incidentes', to='administracion.UsuariosGrexco')),
            ],
        ),
        migrations.CreateModel(
            name='RespuestasIncidentes',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('respuesta', models.TextField()),
                ('incidente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='respuesta', to='usuarios.Incidentes')),
            ],
        ),
        migrations.CreateModel(
            name='TiposIncidentes',
            fields=[
                ('codigo', models.SmallIntegerField(primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='UsuariosSoporteIncidentes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('incidente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='usuarios_soporte', to='usuarios.Incidentes')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='incidentes_soporte', to='administracion.UsuariosGrexco')),
            ],
        ),
        migrations.CreateModel(
            name='UsuariosTecnologiaIncidentes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('incidente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='usuarios_tecnologia', to='usuarios.Incidentes')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='incidentes_tecnologia', to='administracion.UsuariosGrexco')),
            ],
        ),
        migrations.AddField(
            model_name='incidentes',
            name='tipo_incidente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='incidentes', to='usuarios.TiposIncidentes'),
        ),
        migrations.AddField(
            model_name='incidentes',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='incidentes', to='administracion.UsuariosGrexco'),
        ),
        migrations.AddField(
            model_name='adjuntosrespuestasincidentes',
            name='respuesta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='adjuntos', to='usuarios.RespuestasIncidentes'),
        ),
        migrations.AddField(
            model_name='adjuntos',
            name='incidente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='adjuntos', to='usuarios.Incidentes'),
        ),
    ]
