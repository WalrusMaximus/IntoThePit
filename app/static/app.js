$(document).ready(function() {

    // Check for click events on the navbar burger icon
    $(".navbar-burger").click(function() {
  
        // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
        $(".navbar-burger").toggleClass("is-active");
        $(".navbar-menu").toggleClass("is-active");
  
    });

    $(".modal-background").click(function() {
        $(`.is-active`).removeClass("is-active")
    })

    $(".modal-clear").click(function() {
        $(`.is-active`).removeClass("is-active")
    })
    
  });

const confirmModal = (type, id) => {
    $(`#${type}-modal-${id}`).toggleClass("is-active")
    console.log(`${type}-modal-${id}`)
}