$(document).ready(function($) {

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

	/* 
	Verifica que los campos del formulario de contacto NO
	estén vacios.	
	*/ 
	$(".contacto").focusout(function()
		{
   		  var valor = $(this).val();
   		  if (valor.length == 0)
   		   {
   			  $(this).siblings('span').show();
   		   }
   		  else
   		   {
   			  $(this).siblings('span').hide();
   		   };
	    });


	// Envia los datos para el Login
	$("#btnIngresar").click(function(e) 
	{
		e.preventDefault();
		$("#btnIngresar").prop('disabled', true);
		
		var usuario =
		{
			'usuario': $("#usuario").val(),
		    'contraseña': $("#contraseña").val(),
		};

		var data = JSON.stringify(usuario)

		$.ajax(
		{
			url: '',
			type: 'POST',
			dataType: 'json',
			data: data,
		})
		.done(function(data, status)
		{
			window.location.replace(data["url"])
		})
		.fail(function(error, status)
		{

			$('#alertaError').find('#alertaErrorMensaje').text(error.responseText);
            $('#alertaError').show();
			$("#btnIngresar").prop('disabled', false);
		})		
	});

	//Oculta las Alertas
    $('.btnCerrarAlerta').click(function(event) {
        event.preventDefault();
        $(this).parents('div.alert').hide();
    });

});