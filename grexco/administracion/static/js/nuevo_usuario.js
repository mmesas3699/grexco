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
    $('select').change(function (e) { 
       e.preventDefault()
    
       var option = $(this).val()
       if (option == 'none') {
            $('#form-cliente').hide();
            $('#form-soporte').hide();
            $('#form-tecnologia').hide();
            $('#save-user').hide();
       } else if (option == 'cliente') {
            $('#form-cliente').show();
            $('#form-soporte').hide();
            $('#form-tecnologia').hide();
            $('#save-user').show();
       } else if (option == 'soporte') {
            $('#form-soporte').show();
            $('#form-cliente').hide();
            $('#form-tecnologia').hide();
            $('#save-user').show();
       } else {
            $('#form-soporte').hide();
            $('#form-cliente').hide();
            $('#form-tecnologia').show();
            $('#save-user').show();
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
    $("#save-user").click(function(e) 
    {
        e.preventDefault();
        $(this).prop('disabled', true);
        
        var option = $('option:selected').val()
        
        var user = {}

        if (option == 'cliente') {
            user = {
                "username" : $("#username").val(),
                
            }
             
        } else if (option == 'soporte') {
            alert(option)
        } else if(option == 'tecnologia') {
            alert(opcion)
        }

        
        $.ajax(
        {
            url: '',
            type: 'POST',
            dataType: 'json',
            data: user,
            async: 'False',
        })
        .done(function(json, status)
        {
            alert(json["ok"], status);
        })
        .fail(function(e)
        {
            alert(e);
        })
        .always(function()
        {
            alert("complete");
        });
    });

});