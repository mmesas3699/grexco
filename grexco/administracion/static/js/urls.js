/* 
Se definen la variables que almacenan las URLs usadas por la APP.
*/

/* --------------------------------------------------------
				       ADMINISTRACION
-------------------------------------------------------- */

// Base Administración
var urlBaseAdministracion = '/a/' 

// Convenios
var urlConvenios = urlBaseAdministracion + "convenios/"
var urlConveniosNuevo = urlConvenios + "nuevo/"
var urlConveniosAgregar = urlConvenios + "agregar/"
var urlConveniosNoConvenios = urlConvenios + "listado/no-convenios/"
var urlConveniosConsulta = urlConvenios + "consulta/"
var urlConveniosConsultaIndividual = urlConveniosConsulta + "individual/"
var urlConveniosRetirar = urlConvenios + "retirar/"

// Tipos Incidentes
var urlTiposIncidentes = urlBaseAdministracion + "tipos-incidentes/"
var urlTiposIncidentesListado = urlTiposIncidentes + "listado/"

// Aplicaciones
var urlAplicaciones = urlBaseAdministracion + "aplicaciones/"
var urlAplicacionesEliminar = urlAplicaciones + "eliminar/"
var urlAplicacionesListado = urlAplicaciones + "listado/"
var urlAplicacionesNuevo = urlAplicaciones + "nuevo/"

// Prioridades de Respuesta
var urlPrioridadesRespuesta = urlBaseAdministracion + "prioridades-respuesta/"


/* --------------------------------------------------------
						USUARIOS
-------------------------------------------------------- */
// Base Usuarios
var urlBaseUsuarios = "/usuarios/"

// Incidentes
var urlIncidentes = urlBaseUsuarios + "incidentes/"
var urlCodigoIncidentes = urlIncidentes + "codigo/"
var urlConsultaIncidentes = urlIncidentes + "consulta/"
var urlConsultaIncidentesPorUsuario = urlConsultaIncidentes + "por-usuario/"
var urlGuardaIncidentes = urlIncidentes + "guardar/"
var urlIncidentesConsultaIndividualJson = urlConsultaIncidentes + "json/"


/* ------------------------------------------------------
					SOPORTE
------------------------------------------------------ */
// Base Soporte
var urlHomeSoporteView = "/soporte/"

// Soporte
var urlSoporteIncidentes = urlHomeSoporteView + "incidentes/"
var urlListadoIncidentes = urlSoporteIncidentes + "listado/"
var urlSopConInc = urlSoporteIncidentes + "consulta/"
var urlUsuariosSoporte = urlHomeSoporteView + "consulta/usuarios/"
