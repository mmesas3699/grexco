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
    

    // Abre el Modal: modalEditarReporte
    $("#btnEditarReporte").click(function(event) {
        event.preventDefault();
        $("#modalEditarReporte").modal("show");
    });

    // Cierra el Modal: modalEditarReporte
    $("#btnCerrarModal").click(function(event) {
        event.preventDefault();
        $("#modalEditarReporte").modal("hide"); 
    });

    // Cambia el nombre del reporte
    $("#btnGuardar").click(function(event) {
        event.preventDefault();
        var reporte = 
        {
            'id': $("#idReporte").text(),
            'nuevo_nombre': $("#inpNuevoNombreReporte").val(),
        }

        $.ajax({
            url: '/a/reportes/actualizar/',
            type: 'POST',
            dataType: 'json',
            data: reporte,
        })
        .done(function(data) {
            console.log(data);
            $('#alertaOk').text(data['ok']);
            $('#alertaOk').show();
            $('#alertaError').hide();
        })
        .fail(function(error) {
            console.log(error);
            $('#alertaError').text(error.responseJSON['error']);
            $('#alertaError').show();
            $('#alertaOk').hide();
        })
        
    });


    // Recarga la página al cerra el modal: modalEditarReporte
    $('#modalEditarReporte').on('hidden.bs.modal', function (e) {
        e.preventDefault();
        location.reload();
    })


    // Eliminar Reportes
    $("#btnEliminarReporte").click(function(e) {
        e.preventDefault();
        var reporte = {
            'reporte': $("#idReporte").text(),
        }
        var nombreReporte = $('ol.breadcrumb').children('li:last').text();
            
        if (confirm("¿Está seguro de eliminar el Reporte: " + nombreReporte + "?")) {
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
                window.location.replace("/a/reportes/")
            })
            .fail(function(error, status)
            {
                err = error.responseJSON['error']
                $('#alertaEliminarError').find('#alertaEliminarErrorMensaje').text(err);
                $('#alertaEliminarError').show();
                $('#alertaEliminarOK').hide();
            })
        } else {
            alert('No se eliminó ningún Reporte');
        }
    });


    //Oculta las Alertas
    $('.btnCerrarAlerta').click(function(event) {
        event.preventDefault();
        $(this).parents('div.alert').hide();
    });

});