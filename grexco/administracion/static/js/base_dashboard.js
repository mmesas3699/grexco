$(document).ready(function (){
	// Asigna o retira la clase 'active'
    $(".menu-btn").click(function(){
        $(this).toggleClass("active");
		$(this).children('i.arrow').toggle();
    });

});