# Generated by Django 2.0.1 on 2018-05-29 14:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('administracion', '0001_initial'),
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cambios',
            fields=[
                ('codigo', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('descripcion', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='EstadosCambios',
            fields=[
                ('codigo', models.CharField(max_length=1, primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='TiposCambios',
            fields=[
                ('codigo', models.CharField(max_length=1, primary_key=True, serialize=False)),
                ('descripcion', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='VersionesAplicaciones',
            fields=[
                ('id', models.PositiveSmallIntegerField(primary_key=True, serialize=False)),
                ('version', models.CharField(max_length=20)),
                ('commit', models.CharField(max_length=30)),
                ('fecha', models.DateField()),
                ('aplicacion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='versiones', to='administracion.Aplicaciones')),
            ],
        ),
        migrations.CreateModel(
            name='VersionesReportes',
            fields=[
                ('id', models.PositiveSmallIntegerField(primary_key=True, serialize=False)),
                ('version', models.CharField(max_length=20)),
                ('commit', models.CharField(max_length=30)),
                ('fecha', models.DateField()),
                ('reporte', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='versiones', to='administracion.Reportes')),
            ],
        ),
        migrations.AddField(
            model_name='cambios',
            name='estado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='estados_cambios', to='tecnologia.EstadosCambios'),
        ),
        migrations.AddField(
            model_name='cambios',
            name='incidente',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='cambios', to='usuarios.Incidentes'),
        ),
        migrations.AddField(
            model_name='cambios',
            name='tipo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cambios', to='tecnologia.TiposCambios'),
        ),
        migrations.AddField(
            model_name='cambios',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cambios', to='administracion.UsuariosGrexco'),
        ),
        migrations.AddField(
            model_name='cambios',
            name='version_aplicacion',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='cambios', to='tecnologia.VersionesAplicaciones'),
        ),
        migrations.AddField(
            model_name='cambios',
            name='versiones_reportes',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='cambios', to='tecnologia.VersionesReportes'),
        ),
    ]
