from django.urls import path

from . import views

urlpatterns = [
    path('r"^administracion/$"', views.index, name='index'),
    path('contacto/', views.contacto, name='contacto' )
]