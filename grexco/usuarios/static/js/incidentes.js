$(document).ready( function ()
{

    /* Captura la cookie necesaria para el csrf token */    
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
        
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
        
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    // Opciones por default de las tablas
    $.extend($.fn.dataTable.defaults, {
        "paging": false,
        "info": false,
        "language": {
            url: "//cdn.datatables.net/plug-ins/1.10.16/i18n/Spanish.json",
            select: {
                rows: "%d filas seleccionadas"
            }
        },
    });

    // Tabla Incidentes
    var tblIncidentes = $("#tblIncidentes").DataTable({
        searching: false,
        paging: false,
        select: true,
        ajax: {
            url: urlConsultaIncidentesPorUsuario,
            type: "get",
            dataSrc: "incidentes"
        },
        columns: [
            {data: "codigo"},
            {data: "titulo"},
            {data: "aplicacion__nombre"},
            {data: "estado__descripcion"},
            {data: "fecha_creacion"},
        ],
    })

    // Asigna o retira la clase 'selected' al dar clic sobre una fila
    $('#tblAplicaciones tbody, #tblConvenios tbody').on( 'click', 'tr', function () {
        $(this).toggleClass('selected');
    } );

    /* Consulta detalle de la Empresa seleccionada
    $('#btnConsultar').on('click', 'tr', function(event) {
        event.preventDefault();

    });*/

    $('#btnConsultar').click(function(event) {
        event.preventDefault();
        var codigo = $('#tblIncidentes tr.selected td:first-child').text();
        l = window.location.href;
        console.log(l + codigo);
        // window.location.assign(l+'consulta/'+nit);
        console.log(l)
    });

});