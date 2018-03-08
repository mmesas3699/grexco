$(document).ready(function () {
   
    $('select').change(function (e) { 
       e.preventDefault()
    
       var option = $(this).val()
       if (option == 'none') {
            $('#form-cliente').hide();
            $('#form-soporte').hide();
            $('#form-tecnologia').hide();
       } else if (option == 'cliente') {
            $('#form-cliente').show();
            $('#form-soporte').hide();
            $('#form-tecnologia').hide();
       } else if (option == 'soporte') {
            $('#form-soporte').show();
            $('#form-cliente').hide();
            $('#form-tecnologia').hide();
       } else {
            $('#form-soporte').hide();
            $('#form-cliente').hide();
            $('#form-tecnologia').show();
       };    
   });

   	/* 
	Verifica que los campos del formulario de contacto NO
	estén vacios.	
	*/ 
	$(".contacto").focusout(function() {
        var valor = $(this).val();
        if (valor.length == 0) {
            $(this).siblings('span').show();
        }
        else {
            $(this).siblings('span').hide();
        };
    });
   
});