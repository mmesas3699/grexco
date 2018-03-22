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

	// Envia el formulario de Contacto
	$("button").click(function(e) 
	{
		e.preventDefault();
		$("#enviar").prop('disabled', true);
		
		var user = {
						'name': $("#name").val(),
					    'pwd': $("#pwd").val(),
					};

		$.ajax(
		{
			url: '',
			type: 'POST',
			dataType: 'json',
			data: user,
		})
		.done(function(result)
		{
			alert(result);
		})
		.fail(function()
		{
			alert("error");
		})
		.always(function()
		{
			alert("complete");
		});
		
	});
});