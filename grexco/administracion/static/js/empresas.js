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
    var tblEmpresas = $("#tblEmpresas").DataTable({
        "searching": true,
        "paging": true,
        "select": "single",
        "responsive": true,
        "ajax": {
            url: "listado/",
            type: "get",
            dataSrc: "empresas"
        },
        columns: [
            {data: "nit"},
            {data: "nombre"},
            {data: "direccion"},
            {data: "telefono"},
            {data: "plataforma__nombre"},
            {data: "activa"}
        ]
    });

    // Crea para exportar la tabla de Empresas a Excel
    new $.fn.dataTable.Buttons( tblEmpresas, {
        buttons: [
            { 
                extend: 'excel',
                name: 'ExportarExcel',
                className: 'btn-sm btn-success ml-1',
            },
        ]
     } );
 
    // Inserta el boton Excel a la barra de opciones
    tblEmpresas.buttons().container()
        .appendTo( $('#barraOpciones', tblEmpresas.table().container() ) );


    // Abre el modal para crear una Empresa
    $('#btnNuevaEmpresa').click(function(event) {
        event.preventDefault();
        $.get('/a/plataformas/listado/', function(data) {
            var plataformas = data['plataformas'];
            $(plataformas).each(function(index, el) {
                $('#selPlataforma').append(
                        '<option value="'+ this['id']+ '">'+ this['nombre'] + ' : ' + this['version'] +'</option>'
                );
            });
        });
        $('#modalNuevaEmpresa').modal('show');
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

        if ($("#inpActiva").prop("checked")){
            var activa = 'True'
        } else {
            var activa = 'False'
        }

        var data = 
            {
                "nit": $("#inpNit").val(),
                "nombre": $("#inpNombre").val(),
                "direccion": $("#inpDireccion").val(),
                "telefono": $("#inpTelefono").val(),
                "plataforma": $("#selPlataforma").val(),
                "activa": activa,
            };
        
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
    $('#modalNuevaEmpresa').on('hidden.bs.modal', function(event) {
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