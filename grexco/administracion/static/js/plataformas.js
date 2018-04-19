
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

    /* Da las propiedades de DataTables a la tabla seleccionada */
    var table = $('#tabla-plataformas').DataTable({
    	    paging: false,
    	    select: true,
    	    "language": {
                "sProcessing":     "Procesando...",
                "sLengthMenu":     "Mostrar _MENU_ registros",
                "sZeroRecords":    "No se encontraron resultados",
                "sEmptyTable":     "Ningún dato disponible en esta tabla",
                "sInfo":           "",
                "sInfoEmpty":      "Mostrando registros del 0 al 0 de un total de 0 registros",
                "sInfoFiltered":   "(filtrado de un total de _MAX_ registros)",
                "sInfoPostFix":    "",
                "sSearch":         "Buscar:",
                "sUrl":            "",
                "sInfoThousands":  ",",
                "sLoadingRecords": "Cargando...",
                "oPaginate": {
                    "sFirst":    "Primero",
                    "sLast":     "Último",
                    "sNext":     "Siguiente",
                    "sPrevious": "Anterior"
                },
                "oAria": {
                    "sSortAscending":  ": Activar para ordenar la columna de manera ascendente",
                    "sSortDescending": ": Activar para ordenar la columna de manera descendente"
                },
                 select: {
                    rows: "%d filas seleccionadas"
                }
            },
        });


    // Envia los datos por ajax para eliminar la plataforma seleccionada:
    $("#eliminar").click(function(e) 
    {
        e.preventDefault();
       
        var data = table.rows('.selected').data();

        if (data.length == 0) {
            alert('¡No ha seleccionado ninguna plataforma!');
            location.reload();
        } else if (data.length > 1) {
            alert('¡Solo puede eliminar una plataforma a la vez!');
            location.reload();
        } else {

            console.log(data.length)
            
            if (confirm("¿Está seguro de eliminar la plataforma: " + data[0][1] + "?")) {
                var plataformas = {'plataformas': data.toArray()};
                var row = table.row('.selected');
                console.log(row)

                $.ajax(
                {
                    url: '/a/plataformas/eliminar',
                    type: 'POST',
                    dataType: 'json',
                    data: plataformas,
                    async: 'False',
                })
                .done(function(data, status)
                {
                    // console.log(data["ok"], status);
                    $('#alerta-ok').text(data['ok']);
                    row.remove().draw();
                    $('#alerta-ok').show();
                    $('#alerta-error').hide();
                })
                .fail(function(data, status)
                {
                    // console.log(data.responseJSON['error'], status);
                    $('#alerta-error').text(data.responseJSON['error']);
                    $('#alerta-error').show();
                    $('#alerta-ok').hide();
                })
            } else {
                alert('No se eliminó ninguna plataforma');
            }
        }
    });
});