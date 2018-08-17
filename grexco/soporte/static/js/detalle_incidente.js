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

    var codigo = $("i#codigo").text()
    /*$.ajax({
        url: urlIncidentesConsultaIndividualJson + codigo,
        type: 'GET' ,
        dataType: 'json',
    })
    .done(function(data, status) {
        console.log(data);
    })
    .fail(function() {
        alert("error");
    })
    .always(function() {
        alert("complete");
    });*/
    

    // Asigna el caso al Usuario seleccionado.
    $("#btnEnviar").click(function(event) {
        event.preventDefault();
        var frmData = {
            'usuario': $('#selUsuario').val(),
            'incidente': $('#codigo').text(),
            'prioridad': $('#selPrioResp').val()
        }
        var data = JSON.stringify(frmData)
        $.ajax({
            url: '/soporte/asigna/incidentes/soporte/',
            type: 'POST',
            data: data,
        })
        .done(function() {
            alert("success");
        })
        .fail(function() {
            alert("error");
        })     
    });

    // Consulta los usuarios de soporte que estén activos.
    $.get(urlUsuariosSoporte, function(data) {
        var usuarios = data['usuarios'];
        $(usuarios).each(function(index, el) {
            $('#selUsuario').append(
                '<option value="'+ this['username']+ '">'+ this['username'] + '</option>'
            );
        });
    });

    // Consulta las prioridades de respuesta.
    $.get(urlPrioridadesRespuesta, function(data) {
        var prioridades = data['prioridades'];
        $(prioridades).each(function(index, el) {
            $('#selPrioResp').append(
                '<option value="'+ this['codigo']+ '">'+ this['descripcion'] + '</option>'
            );     
        });
    });


});