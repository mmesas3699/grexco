# Generated by Django 2.0.1 on 2018-07-30 12:36

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0021_auto_20180730_1220'),
    ]

    operations = [
        migrations.AddField(
            model_name='adjuntos',
            name='incidente',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='adjuntos', to='usuarios.Incidentes'),
            preserve_default=False,
        ),
    ]
