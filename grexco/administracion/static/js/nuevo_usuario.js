$(document).ready(function () {
   
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


    /*
    Oculta o muestra los formularios dependiendo
    de la opción elegida en el 'select'.
    */
    $('select#tipo-usuario').change(function (e) { 
       e.preventDefault()
    
       var option = $(this).val()
       if (option == 'none') {
            $('#form-cliente').hide();
            $('#form-soporte').hide();
            $('#form-tecnologia').hide();
            $('button#guardar').hide();
       } else if (option == 'cliente') {
            $('#form-cliente').show();
            $('#form-soporte').hide();
            $('#form-tecnologia').hide();
            $('button#guardar').show();
       } else if (option == 'soporte') {
            $('#form-soporte').show();
            $('#form-cliente').hide();
            $('#form-tecnologia').hide();
            $('button#guardar').show();
       } else {
            $('#form-soporte').hide();
            $('#form-cliente').hide();
            $('#form-tecnologia').show();
            $('button#guardar').show();
       };    
   });


   	/* 
	Verifica que los campos del formulario NO
	estén vacios.	
	*/ 
	$("input").focusout(function() {
        var valor = $(this).val();
        if (valor.length == 0) {
            $(this).siblings('span').show();
        }
        else {
            $(this).siblings('span').hide();
        };
    });

    
    // Envia los datos por ajax:
    $("button#guardar").click(function(e) 
    {
        e.preventDefault();
        
        if ($('select#tipo-usuario').val() == 'cliente'){
            data = {
                "tipo_usuario": $('select#tipo-usuario').val(),
                "empresa": $('form#cliente  select#empresa').val(),
                "nombre": $('form#cliente  input#nombre').val(),
                "apellido": $('form#cliente  input#apellido').val(),
                "cargo": $('form#cliente  input#cargo').val(),
                "telefono": $('form#cliente  input#telefono').val(),
                "extension": $('form#cliente  input#extension').val(),
                "email": $('form#cliente  input#email').val(),
                "nombre_usuario": $('form#cliente  input#nombre-usuario').val(),
            }

            console.log(data)

            $.ajax({
                url: '',
                type: 'POST',
                dataType: 'json',
                data: data,
                async: 'False',
            })
            .done(function(msj, status){
                // console.log(msj);
                // console.log(msj.ok);
                $('#alerta-ok').text(msj.ok)
                $('#alerta-err').hide();
                $('#alerta-ok').show();

            })
            .fail(function(err, status){
                // console.log(err);
                $('#alerta-err').text(err.responseJSON['error'])
                $('#alerta-ok').hide();
                $('#alerta-err').show();
            })
             
        } else if (option == 'soporte'){
            alert(option)
        } else if(option == 'tecnologia'){
            alert(option)
        }

    });

});