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
    var tblEmpresas = $("#tblEmpresas").DataTable({
        "searching": true,
        "paging": true,
        "select": "single",
        "responsive": true,
        "ajax": {
            url: "listado/empresas/",
            type: "get",
            dataSrc: "empresas"
        },
        columns: [
            {data: "nit"},
            {data: "nombre"}
        ]
    });

    // Tabla aplicaciones
    var tblAplicaciones = $("#tblAplicaciones").DataTable({
        "searching": false,
        "paging": false,
        "scrollY": '300px',
        "scrollCollapse": true,
        "ajax": {
            url: "/a/aplicaciones/listado/",
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
    $('#btnNuevoConvenio').click(function(event) {
        event.preventDefault();
        $.get('/a/empresas/listado/activas/', function(data) {
            var empresas = data['empresas'];
            $(empresas).each(function(index, el) {
                $('#selEmpresa').append(
                        '<option value="'+ this['nit']+ '">'+ this['nombre'] + '</option>'
                );
            });
        });
        $('#modalNuevoConvenio').modal('show');
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

        var empresa = $("#selEmpresa").val()
        var aplicaciones = tblAplicaciones.rows('.selected').data().toArray();
        var convenios = {
            'empresa': empresa,
            'aplicaciones': aplicaciones,
        }
        var data = JSON.stringify(convenios)

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


    //Al cerrar el modal '#modalNuevoConvenio' borra las opciones del select de 
    //empresas (#selEmpresa). Esto porque cada vez que se abre el modal
    //duplica los valores de las opciones. También oculta las alertas que estén visibles.
    $('#modalNuevoConvenio').on('hidden.bs.modal', function(event) {
        event.preventDefault();
        // Limpia las opciones del select
        $('#selEmpresa').empty();

        // Inserta la opción por defecto.
        $('#selEmpresa').append(
            '<option value="0">Seleccione una empresa</option>'
        );

        // Si llegasen a estar activas oculta las alertas
        $('#alertaOk').hide();
        $('#alertaError').hide();
        tblEmpresas.ajax.reload();
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