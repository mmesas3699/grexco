from django.urls import path
from django.contrib.auth.views import logout

from . import views

app_name = 'administracion'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='admin_login'),
    path('logout', logout, {'next_page': '/'}, name="logout"),
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('plataformas/', views.PlatformView.as_view(), name='plataformas'),
    path('plataformas/nuevo', views.CreatePlatformView.as_view(), name='nueva_plataforma'),
    path('plataformas/eliminar', views.DeletePlatformView.as_view(), name='eliminar_plataforma'),
    path('aplicaciones/', views.AplicationsView.as_view(), name='aplicaciones'),
    path('aplicaciones/nuevo', views.CreateAplicationsView.as_view(), name='nueva_aplicacion'),
    path('usuarios/nuevo/usuario/', views.CreateUserView.as_view(), name='nuevo_usuario'),
    path('usuarios/clientes/', views.ConsultClientsView.as_view(), name='clientes'),
    path('empresas/', views.CompaniesView.as_view(), name='empresas'),
    path('empresas/nuevo', views.CreateCompanyView.as_view(), name='nueva_empresa'),
]
