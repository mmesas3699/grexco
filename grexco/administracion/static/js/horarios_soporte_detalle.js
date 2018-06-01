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
        "select": true,
        "language": {
            url: "//cdn.datatables.net/plug-ins/1.10.16/i18n/Spanish.json",
            select: {
                rows: "%d filas seleccionadas"
            }
        },
    });

    
    // Crea la tabla Nuevo Horario de Soporte
    var tblHorarioSoporte = $('#tblHorariosSoporte').DataTable({
        "searching": false,
        "select": false,
    });

});