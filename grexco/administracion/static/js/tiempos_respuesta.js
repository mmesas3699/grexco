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
    
    // Tabla empresas
    var tblTiemposRespuesta = $("#tblTiemposRespuesta").DataTable({
        "searching": true,
        "select": "single",
        "ajax": {
            url: "/a/tiempos-respuesta/empresas/",
            type: "get",
            dataSrc: "empresas"
        },
        columns: [
            { data: "nit"},
            { data: "nombre"},
        ]
    });

    // Tabla Nuevo tiempo de respuesta
    var tblNuevoTiempoRespuesta = $("#tblNuevoTiempoRespuesta").DataTable({
        "searching": false,
        "select": false,
        "columnDefs": [
            { "visible": false, "targets": 0 }
        ]
    });

    // Al dar doble clic sobre una empresa se redirecciona a la 
    // consulta del detalle de los timepos de respuesta.
    $('#tblTiemposRespuesta').on('dblclick', 'tr', function(event) {
        event.preventDefault();
        var nit = $(this).children('td:first-child').text();
        l = window.location.href;
        console.log(l + nit);
        window.location.assign(l+nit);
    });

    //Abre el modal para capturar los tiempos de respuesta
    $('#btnNuevoTiempoRespuesta').click(function(event) {
        event.preventDefault();
        $.get('/a/empresas/listado/', function(data) {
            var empresas = data['empresas'];
            $(empresas).each(function(index, el) {
                $('#selEmpresa').append(
                        '<option value="'+ this['nit'] + '">'+ this['nombre'] +'</option>'
                );
            });
        });
        $('#modalNuevoTiempoRespuesta').modal('show');
    });

    //Al cerrar el modal 'modalNuevoTiempoRespuesta' borra las opciones del 
    //select de empresas. Esto porque cada vez que se abre el modal duplica los
    //valores de las opciones. También oculta las alertas que estén visibles.
    $('#modalNuevoTiempoRespuesta').on('hidden.bs.modal', function(event) {
        event.preventDefault();
        // Limpia las opciones del select
        $('#selEmpresa').empty();

        // Inserta la opción por defecto.
        $('#selEmpresa').append(
            '<option value="">Seleccione una empresa</option>'
        );

        // Si llegasen a estar activas oculta las alertas
        $('#alertaOk').hide();
        $('#alertaError').hide();
    });

    // Guarda los tiempos de respuesta
    $("#btnGuardar").click(function(event) {
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
        
        // Verifica que ningun dato este vacio
        $('#tblNuevoTiempoRespuesta input').each(function(){
            if ($(this).val() === ""){
                console.log('err') 
            }
        });

        var tiemposRespuesta = {
            'empresa': $("#selEmpresa").val(),
            'alta': $("#inpPrioridadAlta").val(),
            'baja': $("#inpPrioridadMedia").val(),
            'media': $("#inpPrioridadBaja").val()
        }

        $.ajax({
            url: '/a/tiempos-respuesta/nuevo/',
            type: 'POST',
            dataType: 'json',
            data: tiemposRespuesta,
        })
        .done(function(data) {
            $('#alertaOk').find('#alertaOkMensaje').text(data['ok']);
            $('#alertaOk').show();
            $('i.fa-circle-o-notch').hide();
            $("#btnGuardar").prop("disabled", false);
            $('#alertaError').hide();
        })
        .fail(function(error) {
            $('#alertaError').find('#alertaErrorMensaje').text(error.responseJSON['error']);
            $('#alertaError').show();
            $('i.fa-circle-o-notch').hide();
            $("#btnGuardar").prop("disabled", false);
            $('#alertaOk').hide();
        })
        
    });

    // Consulta detalle Horarios de Soporte
    $('#tblHorariosSoporte').on('dblclick', 'tr', function(event) {
        event.preventDefault();
        var nit = $(this).children('td:first-child').text();
        l = window.location.href;
        console.log(l + nit);
        window.location.assign(l+nit);
    });

    //Oculta las Alertas
    $('.btnCerrarAlerta').click(function(event) {
        event.preventDefault();
        $(this).parents('div.alert').hide();
    });

});