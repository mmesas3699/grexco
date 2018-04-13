# Generated by Django 2.0.1 on 2018-04-13 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(db_column='Id', primary_key=True, serialize=False)),
                ('nombre', models.CharField(db_column='Nom', max_length=50)),
                ('telefono', models.BigIntegerField(db_column='Tel')),
                ('empresa', models.CharField(db_column='Emp', max_length=100)),
                ('email', models.EmailField(db_column='Email', max_length=254)),
                ('mensaje', models.CharField(db_column='Msj', max_length=2000)),
                ('fecha', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
