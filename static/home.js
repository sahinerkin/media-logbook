var modal = $(".modal");

$(".subtitle").click(function() {
    modal.addClass("is-active");
});

$(".close-modal").click(function() {
    modal.removeClass("is-active");
});