$(document).ready(function (){
    $(".dropbtn").click(function(){
        $(this).siblings().toggle();
        $(this).toggleClass("active");
    });
});