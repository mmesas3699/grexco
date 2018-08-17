$(document).ready(function() {

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


    var esCoordinador = $("#es_coordinador").text();
    if (esCoordinador === 'True') {
        $('#tblIncidentes').DataTable( {
            "order": [[ 0, "desc" ]],
            "select": "single",
            "ajax": {
                url: urlListadoIncidentes,
                dataSrc: 'incidentes'
            },
            "columns": [
                {data: 'codigo'},
                {data: 'fecha_creacion'},
                {data: 'titulo'},
                {data: 'usuario__usuariosgrexco__empresa__nombre'},
                {data: 'aplicacion__nombre'},
                {data: 'estado__descripcion'}
            ]
        } );
    } else {
        $('#tblIncidentes').DataTable( {
            "order": [[ 0, "desc" ]],
            "select": "single",
            "ajax": {
                url: urlListadoIncidentes,
                dataSrc: 'incidentes'
            },
            "columns": [
                {data: 'incidente__codigo'},
                {data: 'incidente__fecha_creacion'},
                {data: 'incidente__titulo'},
                {data: 'usuario__usuariosgrexco__empresa__nombre'},
                {data: 'incidente__aplicacion__nombre'},
                {data: 'incidente__estado__descripcion'}
            ]
        } );
    }

    

    //  Consulta detalle del incidente seleccionado
    $('#tblIncidentes').on('dblclick', 'tr', function(event) {
        event.preventDefault();
        var codigo = $(this).children('td:first-child').text();;
        window.location.assign(urlSopConInc + codigo);
    });

});