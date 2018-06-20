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
                "sInfoEmpty":      "",
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


    var tblVersiones = $('#tblVersiones').DataTable({
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


// ====================
//   Nueva aplicación  
// ====================

    /* 
    Habilita/Deshabilita el input #nombreAplicacion y muestra/oculta el botón para seleccionar el 
    archivo de Excel.
    */
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

    // Abre el modal para capturar una nueva aplicación
    $('button#nuevo').click(function(event) {
        $('#modalNuevaAplicacion').modal('show')
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
                url: '/a/aplicaciones/nuevo/',
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

    // Al cerrar el modal de Nueva aplicación recarga la página
    $('#modalNuevaAplicacion').on('hide.bs.modal', function (e) {
        location.reload();
    })


// ==================== 
//  Detalle aplicación  
// ==================== 

    // Abre el modal para consultar una aplicación
    $('tr').dblclick(function (event){
        event.preventDefault();
        var id = $(this).children('td:first-child').text();
        
        /* Envia el 'id' por ajax para consultar los datos de la 
        aplicación seleccionada. */ 
        $.ajax({
            url: '/a/aplicaciones/',
            type: 'POST',
            dataType: 'json',
            data: {'id': id},
            async: 'False',
        })
        .done(function(data, status){
            app = data['aplicacion'];
            nombre_app = app['aplicacion'];
            convenios = app['convenios'];
            versiones = app['versiones'];
            version_actual = versiones[0]['version'];
            
            // Versión actual
            $('#tltDetalleAplicacion').text(nombre_app);
            $('#versionActual').text("Versión actual: " + version_actual);

            $(convenios).each(function(){
                // console.log(this['empresa'], this['nit']);
            });

            $('#modalConsultarAplicacion').modal('show');            
        })
        .fail(function(data, status){
            alert(data.responseJSON['error']);
        })
    });


// ======================================
//     Eliminar Aplicación
// ======================================
    
    $("#eliminar").click(function(e) 
    {
        e.preventDefault();
       
        var data = table.rows('.selected').data();

        if (data.length == 0) {
            alert('¡No ha seleccionado ninguna aplicación!');
            location.reload();
        } else if (data.length > 1) {
            alert('¡Solo puede eliminar una plataforma a la vez!');
            location.reload();
        } else {

            // console.log(data.length, data.toArray())
            
            if (confirm("¿Está seguro de eliminar la aplicación: " + data[0][1] + "?")) {
                var plataformas = {'aplicacion': data.toArray()};
                var row = table.row('.selected');
                console.log(row)

                $.ajax(
                {
                    url: '/a/aplicaciones/eliminar/',
                    type: 'POST',
                    dataType: 'json',
                    data: plataformas,
                    async: 'False',
                })
                .done(function(data, status)
                {
                    // console.log(data["ok"], status);
                    $('#alertaEliminarOk').text(data['ok']);
                    row.remove().draw();
                    $('#alertaEliminarOK').show();
                    $('#alertaEliminarError').hide();
                })
                .fail(function(data, status)
                {
                    // console.log(data.responseJSON['error'], status);
                    $('#alertaEliminarError').text(data.responseJSON['error']);
                    $('#alertaEliminarError').show();
                    $('#alertaEliminarOK').hide();
                })
            } else {
                alert('No se eliminó ninguna Aplicación');
            }
        }
    });

});