from django.urls import path

from . import views

app_name = 'administracion'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='AdminLogin'),
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('usuarios/nuevo/', views.CreateUserView.as_view(), name='new-user')
]
