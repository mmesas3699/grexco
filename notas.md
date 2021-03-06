Conectar Mysql y Django: https://www.digitalocean.com/community/tutorials/how-to-create-a-django-app-and-connect-it-to-a-database

Conceder acceso a usuarios a Mysql: https://chartio.com/resources/tutorials/how-to-grant-all-privileges-on-a-database-in-mysql/

- Crear Data base: CREATE DATABASE grexco_pru CHARACTER SET utf8 COLLATE utf8_general_ci;	
- CREATE USER 'sa'@'localhost' IDENTIFIED BY 'Grexco02';
- Dar permisos a un usuario: GRANT ALL PRIVILEGES ON grexco_pru.*  TO 'sa'@'localhost';
Check Mysql services:
	$ sudo service mysql status
	$ sudo service mysql stop
	$ sudo service mysql start


******* Comandos Django **********
# Iniciar un proyecto 
$ django-admin.py startproject mysite

# Iniciar el servidor de Djando 
$ python manage.py runserver

# Para iniciar el servidor en el puerto 8080
$ python manage.py runserver 8080

# Para que este disponible para cualquier equipo de la red
$ python manage.py runserver 0.0.0.0:8000

# Para instalar mysqlclient
$ sudo apt-get install python3-dev libmysqlclient-dev
$ pip install mysqlclient

# Para crear una app 
$ python manage.py startapp aplicacion


****** Registrar una aplicación ******
- En /my-site/my-site/settings.py :
	
	INSTALLED_APPS = [
		'django.contrib.admin',
	    'django.contrib.auth',
	    'django.contrib.contenttypes',
	    'django.contrib.sessions',
	    'django.contrib.messages',
	    'django.contrib.staticfiles',
	>>  'miApp.apps.miAppConfig', 
	>> Especifica el objeto de configuracion de 'mi aplicación (miApp)'. Este se generó en /my-site/miApp/apps.py

******** Migraciones *******
$ python manage.py makemigrations
$ python manage.py migrate


******** Shell para verificar los modelos ********
$ python manage.py shell


******** Enviar correos *********
from django.core.mail import send_mail
send_mail('Subject here', 'Here is the message.', 'from@example.com', ['to@example.com'], fail_silently=False)

- En settings.py:

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'miguel.mesa@grexco.com.co'
EMAIL_HOST_PASSWORD = 'grexco02'
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True


******** Sitio administrador **********
1. Se debe registrar los modelos de cada aplicación en el archivo admin.py correspondiente:

from .models import Author, Genre, Book, BookInstance

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(BookInstance) 


******** Crear un super usuario ********
$ python manage.py createsuperuser

(supergrexco, Gx10admin)


******** Crear usuarios  ********
from django.contrib.auth.models import User
user = User.objects.create_user(username='john', email='lennon@thebeatles.com', password='johnpassword', **extra_fields)

·· Cambiar la contraseña:
	>>> from django.contrib.auth.models import User
	>>> u = User.objects.get(username='john')
	>>> u.set_password('new password')
	>>> u.save()


******** Para que la aplicacion guarde la hora de la ciudad actual en la BD ********

	# Internationalization
	# https://docs.djangoproject.com/en/2.0/topics/i18n/

		LANGUAGE_CODE = 'en-us'

		TIME_ZONE = 'America/Bogota'

		USE_I18N = True

		USE_L10N = True

		USE_TZ = False


******************
	Usuarios
******************

..
Clientes
	user: cliente1
	pass: 123456

	user: cliente2
	pass: 123456

..
Adminstrador
	user: adms
	pass: grexco02

..
Soporte
	
	.Coordinador
		user: soporte
		pass: grexco02

	.No coordinador
		user: soporte2
		pass: grexco02
