$(document).ready(function($) {

	/* 
	Verifica que los campos del formulario de contacto NO
	estén vacios.	
	*/ 
	$(".contacto").focusout(function(){
   		var valor = $(this).val();
   		if (valor.length == 0) {
   			$(this).siblings('span').show();
   		} else {
   			$(this).siblings('span').hide();
   		};
	});
});

$('form').submit(function(){
  var token = $('input[name="csrfmiddlewaretoken"]').prop('value');
  console.log(mensaje)	  
  $.ajax({
    headers: { "X-CSRFToken": token },
	url: '/contacto/',
	type: 'POST',
	dataType: 'json',
	data: {
		    'nombre': $('#nombre').val(),
		    'telefono': $('#telefono').val(),
		    'empresa': $('#empresa').val(),
		    'email': $('#email').val(),
		    'mensaje': $('#mensaje').val()
		  },
	success: function(data){
		$("#mensaje-enviado").show();
	},
	error: function(data){
		$("#mensaje-no-enviado").show;
	}
  });
});