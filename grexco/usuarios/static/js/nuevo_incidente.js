$(document).ready(function() {

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

    var nitEmpresa = $("#nitEmpresa").text();

    // Código de Incidente.
    $.get(urlCodigoIncidentes, function(data) {
    	$("#inpCodigo").val(data['codigo']);
    	$("#codigo").val(data['codigo']);
    });

    // Agrega las aplicaciones que tienen convenio con la empresa.
    $.get(urlConveniosConsultaIndividual + nitEmpresa, function(data) {
    	var convenios = data['convenios'];

    	$.each(convenios, function (i, convenio)
    	{
   			$('#selAplicacion').append($('<option>', { 
        		value: convenio['aplicacion__id'],
        		text : convenio['aplicacion__nombre'] 
    		}));
		});
    });


    // Muestra el nombre de los archivos adjuntos seleccionados
    $("#inpAdjuntos").change(function(event)
    {
    	event.preventDefault();
    	// Vacía el contenedor 
    	$("div#listadoAdjuntos").empty();
    	var input = $(this);
    	var archivos = input[0].files;

    	$.each(archivos, function(index, val)
    	{
    		$("div#listadoAdjuntos").append(
    			'<div class="alert alert-info m-1 p-1" role="alert">' + val.name + '</div>'
    		)
    	});
    });


    // Guarda los datos del Incidente.
    $("#btnGuardar").click(function(event) {
    	// Deshabilita el botón #btnGuardar 
        $("#btnGuardar").prop("disabled", true);

        // Empieza a girar el icono spin
        $('i.fa-circle-o-notch').addClass('fa-spin');
        
        // Muestra el icono spin
        $('i.fa-circle-o-notch').show();
        
        // Si están abiertos las alertas las oculta
        $('#alertaError').hide();
        $('#alertaError').hide();
    	var form = document.getElementById('formIncidente')
        var data = new FormData(form);

	    $.ajax({
	    	url: '',
	    	type: 'POST',
	    	data: data,
	    	processData: false,
			contentType: false
	    })
	    .done(function(data, status) {
	    	console.log(data);
	    	$('#alertaOk').find('#alertaOkMensaje').text(data['ok']);
            $('#alertaOk').show();
            $('i.fa-circle-o-notch').removeClass('fa-spin');        
            $('i.fa-circle-o-notch').hide();
            $("#btnGuardar").prop("disabled", false);
            $('#alertaError').hide();
	    })
	    .fail(function(error, status) {
	    	console.log(error);
            $('#alertaError').find('#alertaErrorMensaje').text(error.responseJSON['error']);
            $('#alertaError').show();
            $('i.fa-circle-o-notch').removeClass('fa-spin'); 
            $('i.fa-circle-o-notch').hide();
            $("#btnGuardar").prop("disabled", false);
            $('#alertaOk').hide();
	    })
	    .always(function() {
	    	console.log("complete");
			$('i.fa-circle-o-notch').removeClass('fa-spin'); 
            $('i.fa-circle-o-notch').hide();
            $("#btnGuardar").prop("disabled", false);
	    });
    });


    //Oculta las Alertas
    $('.btnCerrarAlerta').click(function(event) {
        event.preventDefault();
        $(this).parents('div.alert').hide();
    });

});