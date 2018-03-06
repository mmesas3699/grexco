from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='AdminLogin'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('usuarios/nuevo/', views.NewUserView.as_view(), name='new-user')
]
