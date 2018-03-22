$(document).ready(function (){
    $(".dropbtn").click(function(){
        $(this).siblings().toggle();
        $(this).parents(".items-menu").toggleClass('active');
    });
});