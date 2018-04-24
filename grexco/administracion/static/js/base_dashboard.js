$(document).ready(function (){
	// Asigna o retira la clase 'active'
    $(".menu-btn").click(function(){
        $(this).toggleClass("active");
    });

    // Hace girar la flecha del menu
    $(".menu-btn").click(function(event) {
		$(this).children('i.arrow').toggle();
    });

});