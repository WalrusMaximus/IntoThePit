$(document).ready(function() {

    // Check for click events on the navbar burger icon
    $(".navbar-burger").click(function() {
  
        // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
        $(".navbar-burger").toggleClass("is-active");
        $(".navbar-menu").toggleClass("is-active");
  
    });
    
  });

const confirmRatingDelete = (ratingNum) => {
    $(`#rating-modal-${ratingNum}`).toggleClass("is-active")
}

const cancelRatingDelete = (ratingNum) => {
    $(`#rating-modal-${ratingNum}`).toggleClass("is-active")
}

const confirmAdminDelete = (ratingNum) => {
    $(`#admin-modal-${ratingNum}`).toggleClass("is-active")
}

const cancelAdminDelete = (ratingNum) => {
    $(`#admin-modal-${ratingNum}`).toggleClass("is-active")
}