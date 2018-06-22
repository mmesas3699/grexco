$(document).ready(function () {
   
    /* Captura la cookie necesaria para el csrf token */    
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();
        
    function csrfSafeMethod(method){
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
    $('select#tipo-usuario').change(function (e){ 
       e.preventDefault()
    
       var option = $(this).val()
       if (option == 'none') {
            $("#form-cliente").hide();
            $("#form-soporte").hide();
            $("#form-tecnologia").hide();
            $("#btnGuardar").hide();
            $("div.alert").hide();
       } else if (option == "cliente") {
            $("#form-cliente").show();
            $("#btnGuardar").show();
            $("#form-soporte").hide();
            $("#form-tecnologia").hide();
            $("div.alert").hide();
       } else if (option == "soporte") {
            $("#form-soporte").show();
            $("#btnGuardar").show();
            $("#form-cliente").hide();
            $("#form-tecnologia").hide();
            $("div.alert").hide();
       } else {
            $("#form-tecnologia").show();
            $("#btnGuardar").show();
            $("#form-soporte").hide();
            $("#form-cliente").hide();
            $("div.alert").hide();
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
    $("#btnGuardar").click(function(e) 
    {
        e.preventDefault();
        
        // Deshabilita el botón #btnGuardar 
        $("#btnGuardar").prop("disabled", true);
        
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
        } else if ($("select#tipo-usuario").val() == "soporte"){
            data = {
                "tipo_usuario": $("select#tipo-usuario").val(),
                "nombre": $("form#soporte  input#nombre").val(),
                "apellido": $("form#soporte  input#apellido").val(),
                "extension": $("form#soporte  input#extension").val(),
                "email": $("form#soporte  input#email").val(),
                "nombre_usuario": $("form#soporte  input#nombre-usuario").val(),   
                "es-coordinador": $("form#soporte input#es-coordinador").val(),
            }
        } else if($('select#tipo-usuario').val() == 'tecnologia'){
            data = {
                "tipo_usuario": $("select#tipo-usuario").val(),
                "nombre": $("form#tecnologia  input#nombre").val(),
                "apellido": $("form#tecnologia  input#apellido").val(),
                "extension": $("form#tecnologia  input#extension").val(),
                "email": $("form#tecnologia input#email").val(),
                "nombre_usuario": $("form#tecnologia  input#nombre-usuario").val(),   
                "es-coordinador": $("form#tecnologia input#es-coordinador").val(),
            }
        }
     
        var usuario = JSON.stringify(data)
        $.ajax({
            url: '',
            type: 'POST',
            dataType: 'json',
            data: usuario,
            async: 'False',
        })
        .done(function(data, status){
            $('#alertaOk').find('#alertaOkMensaje').text(data['ok']);
            $('#alertaOk').show();
            $("#btnGuardar").prop("disabled", false);
            $('#alertaError').hide();
        })
        .fail(function(error, status){
            $('#alertaError').find('#alertaErrorMensaje').text(error.responseJSON['error']);
            $('#alertaError').show();
            $("#btnGuardar").prop("disabled", false);
            $('#alertaOk').hide();
        })       
    });

    //Oculta las Alertas
    $('.btnCerrarAlerta').click(function(event) {
        event.preventDefault();
        $(this).parents('div.alert').hide();
    });
});