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

		$.ajax(
		{
			url: '',
			type: 'POST',
			dataType: 'json',
			data: usuario,
		})
		.done(function(data, status)
		{
			console.log(data)
			window.location.replace(data["url"])
		})
		.fail(function(xhr, status)
		{
			console.log(xhr.status, status);
		})		
	});

});