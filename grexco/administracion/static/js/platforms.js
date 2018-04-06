
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
    	paging: false,
    	select: true,
    	"language":
    	{
  			"search": "Buscar",
  			"info": "",
 		}
    });


    // Envia los datos por ajax:
    $("#erase").click(function(e) 
    {
        e.preventDefault();
       
        var data = $("selected").text()

        console.log(data)
        
        $.ajax(
        {
            url: '/a/plataformas/eliminar',
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