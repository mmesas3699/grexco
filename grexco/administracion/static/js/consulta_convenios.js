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

    // Tabla aplicaciones
    var tblAplicaciones = $("#tblAplicaciones").DataTable({
        "searching": false,
        "paging": false,
        "scrollY": "300px",
        "scrollCollapse": true,
        "ajax": {
            url: urlConveniosNoConvenios + $('#nitEmpresa').text() + "/",
            type: "get",
            dataSrc: "aplicaciones"
        },
        columns: [
            {data: "id"},
            {data: "nombre"}
        ]
    });


    // Asigna o retira la clase 'selected' al dar clic sobre una fila
    $('#tblAplicaciones tbody').on( 'click', 'tr', function () {
        $(this).toggleClass('selected');
    } );


    // Abre el modal para crear/asignar aplicaciones a Empresas
    $('#btnEditarConvenios').click(function(event) {
        event.preventDefault();
        $.get('/a/empresas/listado/', function(data) {
            var empresas = data['empresas'];
            $(empresas).each(function(index, el) {
                $('#selEmpresa').append(
                        '<option value="'+ this['nit']+ '">'+ this['nombre'] + '</option>'
                );
            });
        });
        $('#modalEditarConvenios').modal('show');
    });


    // Envia los datos por ajax:
    $("#btnAgregar").click(function(event)
    {
        event.preventDefault();
       
        // Deshabilita el botón #btnAgregar 
        $("#btnAgregar").prop("disabled", true);

        // Empieza a girar el icono spin
        $('i.fa-circle-o-notch').addClass('fa-spin');
        
        // Muestra el icono spin
        $('i.fa-circle-o-notch').show();
        
        // Si están abiertos las alertas las oculta
        $('#alertaError').hide();
        $('#alertaError').hide();

        var empresa = $('#nitEmpresa').text()
        var aplicaciones = tblAplicaciones.rows('.selected').data().toArray();
        var convenios = {
            'empresa': empresa,
            'aplicaciones': aplicaciones,
        }
        var data = JSON.stringify(convenios)

        $.ajax(
        {
            url: '/a/convenios/actualizar/',
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
            $("#btnAgregar").prop("disabled", false);
            $('#alertaError').hide();
        })
        .fail(function(error, status)
        {
            console.log(error)
            $('#alertaError').find('#alertaErrorMensaje').text(error.responseJSON['error']);
            $('#alertaError').show();
            $('i.fa-circle-o-notch').removeClass('fa-spin'); 
            $('i.fa-circle-o-notch').hide();
            $("#btnAgregar").prop("disabled", false);
            $('#alertaOk').hide();
        });

    });


    //Al cerrar el modal '#modalEditarConvenios' borra las opciones del select de 
    $('#modalEditarConvenios').on('hidden.bs.modal', function(event) {
        event.preventDefault();

        // Si llegasen a estar activas oculta las alertas
        $('#alertaOk').hide();
        $('#alertaError').hide();
        location.reload();
    });


    // Consulta detalle de la Empresa seleccionada
    $('#tblEmpresas').on('dblclick', 'tr', function(event) {
        event.preventDefault();
        var nit = $(this).children('td:first-child').text();
        l = window.location.href;
        console.log(l + nit);
        window.location.assign(l+'consulta/'+nit);
    });


    //Oculta las Alertas
    $('.btnCerrarAlerta').click(function(event) {
        event.preventDefault();
        $(this).parents('div.alert').hide();
    });

});