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

    
    //Abre el modal para capturar horarios de soporte
    $('#btnCrearHorarios').click(function(event) {
        event.preventDefault();
        $.get('/a/empresas/listado/', function(data) {
            var empresas = data['empresas'];
            $(empresas).each(function(index, el) {
                $('#selEmpresa').append(
                        '<option value="'+ this['nit'] + '">'+ this['nombre'] +'</option>'
                );
            });
        });
        $('#modalCapturaHorariosSoporte').modal('show');
    });


    //Al cerrar el modal 'modalCapturaHorariosSoporte' borra las opciones del select de 
    //empresas. Esto porque cada vez que se abre el modal duplica los
    //valores de las opciones. También oculta las alertas que estén visibles.
    $('#modalCapturaHorariosSoporte').on('hidden.bs.modal', function(event) {
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


    // Guardar horarios soporte
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
        
        $('#tblNuevoHorarioSoporte input').each(function(){ if ($(this).val() === ""){ console.log('err') }})
        var horariosSoporte = $('#tblNuevoHorarioSoporte input, #selEmpresa').serialize();
        $.ajax({
            url: '/a/horarios-soporte/nuevo/',
            type: 'POST',
            dataType: 'json',
            data: horariosSoporte,
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