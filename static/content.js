var add_modal = $(".add-modal");

$(".add-content").click(function() {
    add_modal.addClass("is-active");
});

$(".close-add-modal").click(function() {
    add_modal.removeClass("is-active");
});

$(".top-button").click(function() {
    $("html, body").animate({ scrollTop: 0 }, "slow");
});

$(".edit-content").click(function(event) {
    var button_id = event.target.id;
    var cnt_id = button_id.split('-')[2];
    
    var edit_modal = $("#edit-modal-".concat(cnt_id));
    $(edit_modal).addClass("is-active");

});


$(".close-edit-modal").click(function(event) {
    var close_id = event.target.id;
    var cnt_id = close_id.split('-')[3];
    var edit_modal = $("#edit-modal-".concat(cnt_id));
    $(edit_modal).removeClass("is-active");
});


var ratingStars = $(".user_rating > .radio");

function setStars(value) {
    
    for (var i = 0; i < value + 1; i++) {
        var currentStarIcon = $(ratingStars[i]).find("i");
        currentStarIcon.removeClass("far");
        currentStarIcon.addClass("fas");
    }

    for (var i = value + 1; i < ratingStars.length; i++) {
        var currentStarIcon = $(ratingStars[i]).find("i");
        currentStarIcon.removeClass("fas");
        currentStarIcon.addClass("far");
    }
}

$(ratingStars).click(function(){
    setStars($(ratingStars).index(this));
});

$("html, body").animate({ scrollTop: document.body.scrollHeight }, "slow");


