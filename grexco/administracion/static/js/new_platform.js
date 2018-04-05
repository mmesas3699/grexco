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
    $("#save").click(function(e) 
    {
        e.preventDefault();
       
        var platform = {
            'name': $('#name').val(),
            'version': $('#version').val(),
        }
        
        $.ajax(
        {
            url: '',
            type: 'POST',
            dataType: 'json',
            data: platform,
            async: 'False',
        })
        .done(function(data, status)
        {
            // alert(data["ok"], status);
            $('.success').show();
            $('.error').hide();
            
        })
        .fail(function(data, status)
        {
            // alert(data.response, status);
            $('.success').hide();
            $('.error').show();
        })
    });

});