# Generated by Django 2.0.1 on 2018-04-23 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administracion', '0003_auto_20180419_1625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plataformas',
            name='id',
            field=models.SmallIntegerField(primary_key=True, serialize=False),
        ),
    ]
