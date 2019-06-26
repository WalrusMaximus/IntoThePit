$(document).ready(function() {

    // Check for click events on the navbar burger icon
    $(".navbar-burger").click(function() {
  
        // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
        $(".navbar-burger").toggleClass("is-active");
        $(".navbar-menu").toggleClass("is-active");
  
    });
    
  });

const confirmRatingDelete = () => {
    $('.modal').toggleClass("is-active")
}

const cancelRatingDelete = () => {
    $('.modal').toggleClass("is-active")

}