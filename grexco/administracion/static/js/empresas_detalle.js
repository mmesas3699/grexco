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

    // Abre el modal para editar la información de una empresa
    $('#btnEditarEmpresa').click(function(event) {
        event.preventDefault();
        $.get('/a/plataformas/listado/', function(data) {
            var plataformas = data['plataformas'];
            $(plataformas).each(function(index, el) {
                $('#selPlataforma').append(
                        '<option value="'+ this['id']+ '">'+ this['nombre'] + ' : ' + this['version'] +'</option>'
                );
            });
        });
        $('#modalEditarEmpresa').modal('show');
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

        var data = 
            {
                "nit": $("#nitEmpresa").text(),
                "direccion": $("#inpDireccion").val(),
                "telefono": $("#inpTelefono").val(),
                "plataforma": $("#selPlataforma").val(),
            };
        
        $.ajax(
        {
            url: '/a/empresas/actualizar/',
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
            $('#alertaError').find('#alertaErrorMensaje').text(error.responseJSON['error']);
            $('#alertaError').show();
            $('i.fa-circle-o-notch').removeClass('fa-spin'); 
            $('i.fa-circle-o-notch').hide();
            $("#btnGuardar").prop("disabled", false);
            $('#alertaOk').hide();
        });

    });


    //Al cerrar el modal 'modalNuevaEmpresa' borra las opciones del select de 
    //plataformas (#selPlataforma). Esto porque cada vez que se abre el modal
    //duplica los valores de las opciones. También oculta las alertas que estén visibles.
    $('#modalEditarEmpresa').on('hidden.bs.modal', function(event) {
        event.preventDefault();
        // Limpia las opciones del select
        $('#selPlataforma').empty();

        // Inserta la opción por defecto.
        $('#selPlataforma').append(
            '<option value="0">Seleccione una plataforma</option>'
        );

        // Si llegasen a estar activas oculta las alertas
        $('#alertaOk').hide();
        $('#alertaError').hide();
        location.reload();
    });

    //Desactiva una empresa
    $('#btnDesactivarEmpresa').click(function(event) {
        event.preventDefault();

        //Deactiva el botón btnDesactivarEmpresa
        $("#btnDesactivarEmpresa").prop("disabled", true);
        
        var empresa = $("p#nombreEmpresa").text()
        var nit = $("#nitEmpresa").text()

        if (confirm("¿Desea desactivar la empresa: " + empresa + "?")) {
            var data = {"nit": nit};
        
            $.ajax(
            {
                url: '/a/empresas/desactivar/',
                type: 'POST',
                dataType: 'json',
                data: data,
                async: 'False',
            })
            .done(function(data, status)
            {
                location.reload()
            })
            .fail(function(error, status)
            {
                $('#alertaEliminarError').find('#alertaEliminarErrorMensaje').text(error.responseJSON['error']);
                $('#alertaEliminarError').show();
                $("#btnDesactivarEmpresa").prop("disabled", false);
                $('#alertaEliminarOk').hide();
            });
        } else {
            $("#btnDesactivarEmpresa").prop("disabled", false);
        }
    });

    //Activa una empresa
    $('#btnActivarEmpresa').click(function(event) {
        event.preventDefault();

        //Deactiva el botón btnDesactivarEmpresa
        $("#btnActivarEmpresa").prop("disabled", true);
        
        var empresa = $("p#nombreEmpresa").text()
        var nit = $("#nitEmpresa").text()

        if (confirm("¿Desea activar la empresa: " + empresa + "?")) {
            var data = {"nit": nit};
        
            $.ajax(
            {
                url: '/a/empresas/activar/',
                type: 'POST',
                dataType: 'json',
                data: data,
                async: 'False',
            })
            .done(function(data, status)
            {
                location.reload()
            })
            .fail(function(error, status)
            {
                $('#alertaEliminarError').find('#alertaEliminarErrorMensaje').text(error.responseJSON['error']);
                $('#alertaEliminarError').show();
                $("#btnDesactivarEmpresa").prop("disabled", false);
                $('#alertaEliminarOk').hide();
            });
        } else {
            $("#btnDesactivarEmpresa").prop("disabled", false);
        }
    });
    //Oculta las Alertas
    $('.btnCerrarAlerta').click(function(event) {
        event.preventDefault();
        $(this).parents('div.alert').hide();
    });

});