$(document).ready( function ()
{
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

    /* Da las propiedades de DataTables a la tabla seleccionada */
    $('#table').DataTable(
    {
    	paging: true,
    	select: true,
    	language:
    	{
            info: "",
  			search: "Buscar",
            select:
            {
                rows:
                {
                    _: "%d Filas seleccionadas",
                    1: "Una fila seleccionada"
                }
            },
            paginate:
            {
                first:    '«',
                previous: '‹',
                next:     '›',
                last:     '»'
            },
            aria:
            {
                paginate:
                {
                    first:    'First',
                    previous: 'Previous',
                    next:     'Next',
                    last:     'Last'
                }
            },
            emptyTable: "No hay datos disponibles"
 		}

    });

    // Envia los datos por ajax:
    $("#btn-save").click(function(event) 
    {
        event.preventDefault();

        var data = 
            {
                "nit": $("#nit").val(),
                "nombre": $("#nombre").val(),
                "direccion": $("#direccion").val(),
                "telefono": $("#telefono").val(),
                "plataforma": $("#plataforma").val(),
                "aplicaciones": $("#aplicaciones").val(),
            };

        // var data = $('#nueva-empresa').serialize(); 
        
        console.log(data)
        // var empresa = JSON.stringify(data);
        // console.log(empresa)
        
        $.ajax(
        {
            url: '/a/empresas/nuevo',
            type: 'POST',
            dataType: 'json',
            data: data,
            async: 'False',
        })
        .done(function(data, status)
        {
            $('#alerta-ok').text(data.responseJSON['ok'])
            $('#alerta-err').hide();
            $('#alerta-ok').show();

        })
        .fail(function(data, status)
        {
            console.log(data.responseJSON)
            $('#alerta-err').text(data.responseJSON['error'])
            $('#alerta-ok').hide();
            $('#alerta-err').show();
        });

    });
});