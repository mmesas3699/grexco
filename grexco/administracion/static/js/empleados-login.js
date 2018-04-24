$(document).ready(function() {
    
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

    $('button#ingresar').click(function(event) {
        event.preventDefault();


        var datos_usuario = {
            "nombre": $('input#usuario').val(),
            "contraseña": $('input#contraseña').val()
        }

        console.log(datos_usuario);

       $.ajax(
            {
                url: '',
                type: 'POST',
                dataType: 'json',
                data: datos_usuario,
                async: 'False',
            })
            .done(function(data, status)
            {
                window.location.replace("/a/");
                // console.log(data["ok"], status);
            })
            .fail(function(data, status)
            {
                // console.log(data.responseJSON['error'], status);
                $('div.alert').show();
            })
    });
});
