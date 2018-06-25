"""aaaa."""
from django.contrib.auth.views import logout
from django.urls import path

from . import views

app_name = 'administracion'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path(
        'aplicaciones/',
        views.AplicationsView.as_view(),
        name='aplicaciones'
    ),
    path(
        'aplicaciones/eliminar/',
        views.DeleteAplicationsView.as_view(),
        name='eliminar_aplicacion'
    ),
    path(
        'aplicaciones/listado/',
        views.ListadoAplicacionesView.as_view(),
        name='listado_aplicaciones'
    ),
    path(
        'aplicaciones/listado/excel/',
        views.ListExcelAplicationsView.as_view(),
        name='listado_aplicaciones_excel'
    ),
    path(
        'aplicaciones/nuevo/',
        views.CreateAplicationsView.as_view(),
        name='nueva_aplicacion'
    ),
    path('convenios/', views.ConveniosView.as_view(), name='convenios'),
    path(
        'convenios/agregar/',
        views.ConveniosAgregarView.as_view(),
        name='convenios_actualizar'
    ),
    path(
        'convenios/consulta/<str:nit>/',
        views.ConsultaConveniosView.as_view(),
        name='convenios_consulta'
    ),
    path(
        'convenios/consulta/individual/<str:nit>',
        views.ConveniosConsultaIndividualView.as_view()
    ),
    path(
        'convenios/retirar/',
        views.ConveniosRetirarView.as_view(),
        name='convenios_eliminar'
    ),
    path(
        'convenios/listado/empresas/',
        views.ListadoConveniosEmpresasView.as_view(),
        name='convenios_listado'
    ),
    path(
        'convenios/listado/no-convenios/<str:nit>/',
        views.ListadoNoConveniosEmpresasView.as_view(),
        name='no_convenios_listado'
    ),
    path(
        'convenios/nuevo/',
        views.CrearConveniosView.as_view(),
        name='convenios_nuevo'
    ),
    path('empresas/', views.CompaniesView.as_view(), name='empresas'),
    path(
        'empresas/actualizar/',
        views.ActualizaEmpresaView.as_view(),
        name='empresas_actualizar'
    ),
    path(
        'empresas/consulta/<str:nit>/',
        views.ConsultaEmpresaView.as_view(),
        name='consulta_empresas'
    ),
    path(
        'empresas/activar/',
        views.ActivaEmpresasView.as_view(),
        name='empresas_activar'
    ),
    path(
        'empresas/desactivar/',
        views.DesactivaEmpresasView.as_view(),
        name='empresas_desactivar'
    ),
    path(
        'empresas/listado/',
        views.ListadoBasicoEmpresasView.as_view(),
        name='lista_empresas'
    ),
    path(
        'empresas/listado/activas/',
        views.ListadoEmpresasActivas.as_view(),
        name='empresas_listado_activas'
    ),
    path(
        'empresas/nuevo/',
        views.CrearEmpresaView.as_view(),
        name='nueva_empresa'
    ),
    path(
        'horarios-soporte/',
        views.HorariosSoporteView.as_view(),
        name='horarios_soporte'
    ),
    path(
        'horarios-soporte/<int:nit>/',
        views.ConsultaHorariosSoporte.as_view(),
        name='horarios-soporte-consulta'
    ),
    path(
        'horarios-soporte/nuevo/',
        views.CrearHorariosSoporte.as_view(),
        name='nuevo_horario_soporte'
    ),
    path('plataformas/', views.PlataformasView.as_view(), name='plataformas'),
    path(
        'plataformas/eliminar/',
        views.EliminarPlataformasView.as_view(),
        name='eliminar_plataforma'
    ),
    path(
        'plataformas/listado/',
        views.ListadoBasicoPlataformasView.as_view(),
        name='listado_plataformas'
    ),
    path(
        'plataformas/nuevo/',
        views.CrearPlataformasView.as_view(),
        name='nueva_plataforma'
    ),
    path(
        'prioridades-respuesta/',
        views.PrioridadesRespuestaView.as_view(),
        name='prioridades_respuesta'
    ),
    path('reportes/', views.ReportsView.as_view(), name='reportes'),
    path(
        'reportes/nuevo/',
        views.CreateReportsView.as_view(),
        name='nuevo_reporte'
    ),
    path(
        'reportes/<int:id>/',
        views.DetailReportView.as_view(),
        name='detalle_reporte'
    ),
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
        'tipos-incidentes/',
        views.TiposIncidentesView.as_view(),
        name='tipos_incidentes'
    ),
    path(
        'tipos-incidentes/listado/',
        views.TiposIncidentesListadoView.as_view(),
        name='tipos_incidentes_listado'
    ),
    path(
        'tipos-incidentes/nuevo/',
        views.TiposIncidentesNuevoView.as_view(),
        name='tipos_incidentes_nuevo'
    ),
    path(
        'tipos-incidentes/eliminar/',
        views.TiposIncidentesEliminar.as_view(),
        name='tipos_incidentes_eliminar'
    ),
    path(
        'usuarios/nuevo/usuario/',
        views.CrearUsuariosView.as_view(),
        name='nuevo_usuario'
    ),
    path(
        'usuarios/clientes/',
        views.ConsultClientsView.as_view(),
        name='clientes'
    ),
]
