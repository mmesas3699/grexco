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
    var table = $('#tabla-aplicaciones').DataTable({
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

    // Abre el modal para capturar una nueva aplicación
    $('button#nuevo').click(function(event) {
        $('#modalNuevaAplicacion').modal('show')
    });

    // Al cerrar el modal recarga la página
    $('#modalNuevaAplicacion').on('hide.bs.modal', function (e) {
        location.reload();
    })

    // Habilita/Deshabilita el input #nombreAplicacion y muestra u oculta el botón para seleccionar el 
    // archivo de Excel.
    $('#checkExcel').change(function(event) {
        // console.log('cambio');
        if (this.checked) {
            // console.log('on')
            $('input#nombreAplicacion').attr('disabled', 'true');
            $('div#seleccionarArchivo').show();
        }
        else {
            // console.log('off');
            $('input#nombreAplicacion').removeAttr('disabled');
            $('div#seleccionarArchivo').hide();
        }
    });

    // Guarda los datos de la aplicación:
    $("#guardarNuevaAplicacion").click(function(e) 
    {
        var data = new FormData();
        var file = document.getElementById('inpFile').files[0];
        // Por archivo de Excel
        if ($('#checkExcel').prop('checked')) {
            data.append('archivo', file)  
            console.log(data);
            $.ajax(
            {
                url: '/a/aplicaciones/nuevo',
                type: 'POST',
                processData: false,
                contentType: false,
                dataType: 'multipart/form-data',
                data: data,
                async: 'False',
            })
            .done(function(data, status)
            {
                // console.log(data["ok"], status);
                $('#alerta-ok').text(data['ok']);
                $('#alerta-ok').show();
                $('#alerta-error').hide();
            })
            .fail(function(data, status)
            {
                var error =  $.parseJSON(data.responseText);
                // console.log(error)
                var apps = error['error']['aplicaciones']
                console.log(apps)
                $('div#alerta-error').html(
                    "<p> " + error['error']['respuesta'] + "</p>"
                );
                $(apps).each(function(){
                    // console.log(this['err']);
                    $('div#alerta-error').append(
                        "<p> " + this['err'] + " : <b>" + this['app'] + "</b> </p>"
                    );
                });
                $('#alerta-error').show();
                $('#alerta-ok').hide();
            })
        } else {
        // Individualmente
            data = {'nombre': $('input#nombreAplicacion').val()}
            console.log(data);
            $.ajax(
            {
                url: '/a/aplicaciones/nuevo',
                type: 'POST',
                dataType: 'json',
                data: data,
                async: 'False',
            })
            .done(function(data, status)
            {
                // console.log(data["ok"], status);
                $('#alerta-ok').text(data['ok']);
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
        }
    });


});