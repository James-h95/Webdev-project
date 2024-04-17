$(document).ready(function () {
    $("#toggleBar").on("click", function() {
        $('.sidebar').width('250px');
        $('#toggleBar').css('opacity', '0');
    });

    $(".sidebar-toggler").on("click", function(){
        $('.sidebar').width('0');
        $('#toggleBar').css('opacity', '100');
    });
});
