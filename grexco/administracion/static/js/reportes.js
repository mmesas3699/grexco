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
        paging: false,
        select: true,
        "language": {
            url: "//cdn.datatables.net/plug-ins/1.10.16/i18n/Spanish.json",
            select: {
                rows: "%d filas seleccionadas"
            }
        },
    });


    // Al cargar la página trae por Ajax el listado de Reportes  
    var tblReportes = $("#tblReportes").DataTable({
        ajax: {
            url: '/a/reportes/',
            type: 'post',
            dataSrc: ''
        },
        columns: [
            { data: 'id' },
            { data: 'nombre' },
            { data: 'aplicacion__nombre' }
        ]
    });
    

    //Abre el modal para capturar un nuevo Reporte
    $('#nuevoReporte').click(function(event) {
        event.preventDefault();
        
        //Trae el listado de aplicaciones para asociar al Reporte
        $.ajax({
            url: '/a/aplicaciones/listado',
            type: 'POST',
            dataType: 'json',
            data: {tipo: 'listado'},
        })
        .done(function(data) {
            //Inserta el listado de aplicaciones en el 'select'
            $(data).each(function(index, el) {
                $('#selectAplicacion').append(
                        '<option value="'+ this['id'] + '">'+ this['nombre'] +'</option>'
                );
            });
            $('#modalNuevoReporte').modal('show');
        })
        .fail(function() {
            console.log("error");
        })

    });


    //Al cerrar el modal 'nuevoReporte' borra las opciones del select de 
    //aplicaciones. Esto porque cada vez que se abre el modal duplica los
    //valores de las opciones. También limpia el formulario 'frmNuevoReporte'
    //y oculta las alertas que estén visibles.
    $('#modalNuevoReporte').on('hidden.bs.modal', function(event) {
        event.preventDefault();
        $('#selectAplicacion').empty();
        $('#selectAplicacion').append(
            '<option value="">Seleccione una aplicación</option>'
        );
        $('#alertaOk').hide();
        $('#alertaError').hide();
        $('#frmNuevoReporte').trigger('reset');
    });


    //Oculta o Muestra los contenedores para capturar los reportes de forma
    //individual o por excel.
    $('#checkExcel').change(function(event) {
        event.preventDefault();
        if (this.checked) {
            $('#containerIndividual').hide();
            $('#containerExcel').show();
        } else {
            $('#containerIndividual').show();
            $('#containerExcel').hide();
        }
    });


    //Envia los datos del nuevo Reporte para ser grabados en la BD
    $('#btnGuardarReporte').click(function(event) {
        event.preventDefault();

        if ($('#checkExcel').prop('checked')) {
            var data = new FormData();
            var archivo = document.getElementById('inpNuevoReporteExcel').files[0];

            data.append('archivo', archivo)
            data.append('tipo', 'excel')
            $.ajax(
            {
                url: 'nuevo/',
                type: 'POST',
                processData: false,
                contentType: false,
                // dataType: 'multipart/form-data',
                data: data,
                async: 'False',
            })
            .done(function(data, status)
            {
                console.log(data["ok"], status);
                $('#alertaOk').text(data['ok']);
                $('#alertaOk').show();
                $('#alertaError').hide();
                tblReportes.ajax.reload();
            })
            .fail(function(data, status)
            {
                var error =  $.parseJSON(data.responseText);
                // console.log(error)
                var reportes = error['error']['reportes']
                console.log(reportes)
                $('div#alertaError').html(
                    "<p> " + error['error']['respuesta'] + "</p>"
                );
                $(reportes).each(function(){
                    // console.log(this['err']);
                    $('div#alertaError').append(
                        "<p> " + this['err'] + " : <b>" + this['reporte'] + "</b> </p>"
                    );
                });
                $('#alertaError').show();
                $('#alertaOk').hide();
            })
        } else {
            var data = {
                    'tipo': 'individual',
                    'nombre': $('#inputNombreReporte').val(),
                    'aplicacion': $('#selectAplicacion').val()
                };
 
            $.ajax({
                url: 'nuevo/',
                type: 'POST',
                dataType: 'json',
                data: data,
            })
            .done(function(data) {
                // console.log(data);
                $('#alertaOk').find('#alertaOkMensaje').text(data['ok']);
                $('#alertaError').hide();
                $('#alertaOk').show();
                tblReportes.ajax.reload();
            })
            .fail(function(err) {
                // console.log(err.responseJSON['error']);
                var msjError = err.responseJSON['error']
                $('#alertaError').find('#alertaErrorMensaje').text(msjError);
                $('#alertaOk').hide();
                $('#alertaError').show();
            })
            
        }
    });


    // Eliminar Reportes
    $("#eliminarReporte").click(function(e)
    {
        e.preventDefault();
       
        var data = tblReportes.rows('.selected').data();

        if (data.length == 0) {
            alert('¡No ha seleccionado ningún Reporte!');
            location.reload();
        } else if (data.length > 1) {
            alert('¡Solo puede eliminar un Reporte a la vez!');
            location.reload();
        } else {

            // console.log(data.length, data.toArray())
            
            if (confirm("¿Está seguro de eliminar el Reporte: " + data[0]['nombre'] + "?")) {
                var reporte = {'reporte': data[0]['id']};
                console.log(reporte)
                var row = tblReportes.row('.selected');

                $.ajax(
                {
                    url: '/a/reportes/eliminar/',
                    type: 'POST',
                    dataType: 'json',
                    data: reporte,
                    async: 'False',
                })
                .done(function(data, status)
                {
                    // console.log(data["ok"], status);
                    $('#alertaEliminarOk').find('#alertaEliminarOkMensaje').text(data['ok']);
                    $('#alertaEliminarOk').show();
                    $('#alertaEliminarError').hide();
                    row.remove().draw();
                })
                .fail(function(data, status)
                {
                    console.log(data.responseJSON['error'], status);
                    $('#alertaEliminarError').find('#alertaEliminarErrorMensaje').text(msjError);
                    $('#alertaEliminarError').show();
                    $('#alertaEliminarOK').hide();
                })
            } else {
                alert('No se eliminó ningún Reporte');
            }
        }
    });


    //Oculta las Alertas
    $('.btnCerrarAlerta').click(function(event) {
        event.preventDefault();
        $(this).parents('div.alert').hide();
    });

});