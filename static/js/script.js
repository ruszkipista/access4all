//Responsive hamburger menu
$(document).ready(function () {
    $('.header-burger').click(function (event) {
        $('.header-burger, .header-menu').toggleClass('active');
        $('body').toggleClass('lock')
    });
    $(".copyright").text(new Date().getFullYear())
});