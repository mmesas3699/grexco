$(document).ready(function (){

    $(".menu-btn").click(function(){
        $(this).toggleClass("active");
    });

    $(".menu-btn").click(function(event) {
		$(this).children('i.arrow').toggle();
    });

});