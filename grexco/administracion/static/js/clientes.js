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

    $('#tabla-clientes').DataTable({
        paging: true,
        language:{
            info: "",
            search: "Buscar",
            paginate:{
                first:    '«',
                previous: '‹',
                next:     '›',
                last:     '»'
            },
            aria:{
                paginate:{
                    first:    'First',
                    previous: 'Previous',
                    next:     'Next',
                    last:     'Last'
                }
            },
            emptyTable: "No hay datos disponibles"
        }
    });


    $('tbody tr').click(function(event) {
        event.preventDefault();

        var nombre_usuario = $(this).children('td#nombre-usuario').text();
        console.log(nombre_usuario);

        $('h5.modal-title').text(nombre_usuario);

        $.ajax({
            url: '',
            type: 'POST',
            dataType: 'json',
            data: {'nombre_usuario': nombre_usuario},
        })
        .done(function(data) {
            console.log(data);
        })
        .fail(function(error) {
            console.log(error);
        })
        .always(function() {
            console.log("complete");
        });
        
        $('#myModal').modal('show');
    });
});
