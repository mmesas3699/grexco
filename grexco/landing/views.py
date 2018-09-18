from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.mail import send_mail

from .models import Contact


# Create your views here.

def index(request):
    return render(request, 'landing/otro_index.html')


def contacto(request):
    body = dict(request.POST)

    cliente = body['nombre'][0]
    telefono = int(body['telefono'][0])
    empresa = body['empresa'][0]
    email = body['email'][0]
    mensaje = body['mensaje'][0]

    data = {'cliente': cliente, 'telefono': telefono, 'empresa': empresa,
            'email': email, 'mensaje': mensaje}

    # Guarda el mensaje en la BD
    mensaje = Contact(
        nombre=cliente,
        telefono=telefono,
        empresa=empresa,
        email=email,
        mensaje=mensaje)

    mensaje.save()

    # Envio de correo
    send_mail(
        'TIENE UN MENSAJE NUEVO',
        """
        CLIENTE: {cliente}
        TELEFONO: {telefono}
        EMPRESA: {empresa}
        EMAIL: {email}
        MENSAJE: {mensaje}
        """.format(**data),
        'miguel.mesa@grexco.com.co',
        ['soporte@grexco.com.co'],
        fail_silently=False,
    )

    respuesta = {'cliente': body}

    return JsonResponse(respuesta)
