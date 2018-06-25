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

    // Tabla empresas
    var tblTiposIncidentes = $("#tblTiposIncidentes").DataTable({
        "searching": true,
        "paging": true,
        "select": "single",
        "responsive": true,
        "ajax": {
            url: "/a/tipos-incidentes/listado/",
            type: "get",
            dataSrc: "tipos-incidentes"
        },
        columns: [
            {data: "id"},
            {data: "descripcion"}
        ]
    });


    // Asigna o retira la clase 'selected' al dar clic sobre una fila
    $('#tblTiposIncidentes tbody').on( 'click', 'tr', function () {
        $(this).toggleClass('selected');
    } );


    // Abre el modal para crear/asignar aplicaciones a Empresas
    $('#btnNuevoTipoIncidente').click(function(event) {
        event.preventDefault();
        $('#modalNuevoTipoIncidente').modal('show');
    });


    // Envia los datos por ajax:
    $("#btnGuardar").click(function(event) 
    {
        event.preventDefault();
       
        // Deshabilita el botón #btnGuardar 
        $("#btnGuardar").prop("disabled", true);

        // Empieza a girar el icono spin
        $('i.fa-circle-o-notch').addClass('fa-spin');
        
        // Muestra el icono spin
        $('i.fa-circle-o-notch').show();
        
        // Si están abiertos las alertas las oculta
        $('#alertaError').hide();
        $('#alertaError').hide();

        var tipo_incidente = {
            "tipo_incidente": $("#inpTipoIncidente").val()
        }
        var data = JSON.stringify(tipo_incidente)

        $.ajax(
        {
            url: 'nuevo/',
            type: 'POST',
            dataType: 'json',
            data: data,
            async: 'False',
        })
        .done(function(data, status)
        {
            $('#alertaOk').find('#alertaOkMensaje').text(data['ok']);
            $('#alertaOk').show();
            $('i.fa-circle-o-notch').removeClass('fa-spin');        
            $('i.fa-circle-o-notch').hide();
            $("#btnGuardar").prop("disabled", false);
            $('#alertaError').hide();
        })
        .fail(function(error, status)
        {
            console.log(error)
            $('#alertaError').find('#alertaErrorMensaje').text(error.responseJSON['error']);
            $('#alertaError').show();
            $('i.fa-circle-o-notch').removeClass('fa-spin'); 
            $('i.fa-circle-o-notch').hide();
            $("#btnGuardar").prop("disabled", false);
            $('#alertaOk').hide();
        });

    });


    $('#modalNuevoTipoIncidente').on('hidden.bs.modal', function(event) {
        event.preventDefault();

        $('#alertaOk').hide();
        $('#alertaError').hide();
        tblTiposIncidentes.ajax.reload();
    });


    // Consulta detalle de la Empresa seleccionada
    $('#tblTiposIncidentes').on('dblclick', 'tr', function(event) {
        event.preventDefault();
        var nit = $(this).children('td:first-child').text();
        l = window.location.href;
        console.log(l + nit);
        window.location.assign(l+'consulta/'+nit);
    });


    // Eliminar
    $("#btnEliminar").click(function(e) 
    {
        e.preventDefault();
       
        var data = tblTiposIncidentes.rows('.selected').data();

        if (data.length == 0) {
            alert('¡No ha seleccionado ningún Tipo de incidente!');
            location.reload();
        } else if (data.length > 1) {
            alert('¡Solo puede eliminar uno a la vez!');
            location.reload();
        } else {
            if (confirm("¿Está seguro de eliminar el tipo de incidente: " + data[0]['descripcion'] + "?")) {
                var tipo = {'tipo_incidente': data[0]['id']};
                var data = JSON.stringify(tipo)
                var row = tblTiposIncidentes.row('.selected');

                $.ajax(
                {
                    url: '/a/tipos-incidentes/eliminar/',
                    type: 'POST',
                    dataType: 'json',
                    data: data,
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

    //Oculta las Alertas
    $('.btnCerrarAlerta').click(function(event) {
        event.preventDefault();
        $(this).parents('div.alert').hide();
    });

});