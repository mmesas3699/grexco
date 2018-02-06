from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.mail import send_mail

from .models import Contact

# Create your views here.

def index(request):
    return render(request, 'landing/index.html')

def contacto(request):
	cliente = request.POST.get('nombre')
	telefono = request.POST.get('telefono')
	empresa = request.POST.get('empresa')
	email = request.POST.get('email')
	mensaje = request.POST.get('mensaje')	

	# Guarda el mensaje en la BD

	mensaje = Contact(
		nombre=cliente,
		telefono=telefono,
		empresa=empresa,
		email=email,
		mensaje=mensaje)

	mensaje.save()

	# Envia correo para avisar de un nuevo mensaje
	send_mail(
		'{} escribio un mensaje'.format(cliente),
		""" CLIENTE: {}
		    TELEFONO: {}
		    EMPRESA: {}
		    EMAIL: {}
		    MENSAJE: {} """.format(cliente, telefono, empresa, email, mensaje),
		'miguel.mesa@grexco.com.co',
		['mmesas369@gmail.com'],
		fail_silently=False,
		)	
	respuesta = {'ok': 'OK'}
	return JsonResponse(respuesta)
