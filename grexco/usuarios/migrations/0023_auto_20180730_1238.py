# Generated by Django 2.0.1 on 2018-07-30 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0022_adjuntos_incidente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adjuntos',
            name='incidente',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='adjuntos', to='usuarios.Incidentes'),
        ),
    ]