from django.urls import path

from . import views

app_name = 'administracion'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='AdminLogin'),
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('usuarios/nuevo/usuario/', views.CreateUserView.as_view(), name='nuevo_usuario'),
    path('usuarios/clientes/', views.ConsultClientsView.as_view(), name='clientes'),
    path('plataformas/', views.PlatformView.as_view(), name='plataformas'),
    path('plataformas/nuevo', views.CreatePlatformView.as_view(), name='nueva_plataforma'),
    path('plataformas/eliminar', views.DeletePlatformView.as_view(), name='eliminar_plataforma'),
    path(
        'empresas/',
        views.CompaniesView.as_view(),
        name='empresas'
    ),
    path(
        'empresas/nuevo',
        views.CreateCompanyView.as_view(),
        name='nueva_empresa'
    )
]
