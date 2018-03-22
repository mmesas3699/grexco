
$(document).ready(function($) {

	$.ajaxSetup(
	{ 
      beforeSend: function(xhr, settings)
      {
        function getCookie(name)
        {
          var cookieValue = null;
          if (document.cookie && document.cookie != '')
          {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++)
            {
              var cookie = jQuery.trim(cookies[i]);
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) == (name + '='))
              {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
              }
            }
          }
          return cookieValue;
        }
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url)))
        {
          // Only send the token to relative URLs i.e. locally.
          xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
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

	// Envia el formulario de Contacto
	$("form").submit(function(e) 
	{
		e.preventDefault();
		$("#enviar").prop('disabled', true);
		
		var cliente = {
						'nombre': $("#nombre").val(),
					    'telefono': $("#telefono").val(),
					    'empresa': $("#empresa").val(),
					    'email': $("#email").val(),
					    'mensaje': $("#mensaje").val()
					   };

		$.ajax(
		{
			url: 'contacto/',
			type: 'POST',
			dataType: 'json',
			data: cliente,
		})
		.done(function(result)
		{
			// alert(result);
			$("#mensaje-enviado").show();
			$("#enviar").prop('disabled', false);
		})
		.fail(function()
		{
			// alert("error");
			 $("#mensaje-no-enviado").show();
			 $("#enviar").prop('disabled', false);
		})
		.always(function()
		{
			// alert("complete");
		});
		
	});
});


