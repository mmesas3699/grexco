from django.contrib.auth.views import logout
from django.urls import path

from . import views

app_name = 'administracion'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path(
        'aplicaciones/', views.AplicationsView.as_view(), name='aplicaciones'),
    path(
        'aplicaciones/nuevo',
        views.CreateAplicationsView.as_view(),
        name='nueva_aplicacion'),
    path(
        'aplicaciones/eliminar',
        views.DeleteAplicationsView.as_view(),
        name='eliminar_aplicacion'),
    path(
        'aplicaciones/listado', views.ListAplicationsView.as_view(),
        name='listado_aplicaciones'),
    path(
        'aplicaciones/listado/excel/',
        views.ListExcelAplicationsView.as_view(),
        name='listado_aplicaciones_excel'),
    path('empresas/', views.CompaniesView.as_view(), name='empresas'),
    path(
        'empresas/nuevo',
        views.CreateCompanyView.as_view(),
        name='nueva_empresa'),
    path(
        'empresas/listado/',
        views.BasicListCompanyView.as_view(),
        name='lista_empresas'),
    path(
        'horarios-soporte/',
        views.HorariosSoporteView.as_view(),
        name='horarios_soporte'),
    path(
        'horarios-soporte/nuevo/',
        views.CrearHorariosSoporte.as_view(),
        name='nuevo_horario_soporte'),
    path(
        'horarios-soporte/<int:nit>',
        views.ConsultaHorariosSoporte.as_view(),
        name='horarios-soporte-consulta'
    ),
    path('login/', views.LoginView.as_view(), name='admin_login'),
    path('logout', logout, {'next_page': '/'}, name="logout"),
    path('plataformas/', views.PlatformView.as_view(), name='plataformas'),
    path(
        'plataformas/nuevo', views.CreatePlatformView.as_view(),
        name='nueva_plataforma'),
    path(
        'plataformas/eliminar', views.DeletePlatformView.as_view(),
        name='eliminar_plataforma'),
    path(
        'prioridades-respuesta/',
        views.PrioridadesRespuestaView.as_view(),
        name='prioridades_respuesta'
    ),
    path(
        'reportes/', views.ReportsView.as_view(), name='reportes'),
    path(
        'reportes/nuevo/',
        views.CreateReportsView.as_view(),
        name='nuevo_reporte'),
    path(
        'reportes/<int:id>/',
        views.DetailReportView.as_view(),
        name='detalle_reporte'),
    path(
        'reportes/eliminar/',
        views.DeleteReportsView.as_view(),
        name='eliminar_reporte'
    ),
    path(
        'reportes/actualizar/',
        views.UpdateReportsView.as_view(),
        name='actualizar_reporte'
    ),
    path(
        'tiempos-respuesta/',
        views.TiemposRespuestaView.as_view(),
        name='tiempos_respuesta'
    ),
    path(
        'tiempos-respuesta/consulta/<int:nit>/',
        views.ConsultaTiemposRespuestaView.as_view(),
        name='tiempos_respuesta_consulta'
    ),
    path(
        'tiempos-respuesta/empresas/',
        views.TiemposRespuestaEmpresas.as_view(),
        name='tiempos_respuesta_empresas'
    ),
    path(
        'tiempos-respuesta/nuevo/',
        views.CrearTiemposRespuestaView.as_view(),
        name='tiempos_respuesta_nuevo'
    ),
    path(
        'usuarios/nuevo/usuario/', views.CreateUserView.as_view(),
        name='nuevo_usuario'),
    path(
        'usuarios/clientes/', views.ConsultClientsView.as_view(),
        name='clientes'),
]
