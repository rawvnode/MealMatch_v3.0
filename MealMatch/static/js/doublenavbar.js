/**
 * Created by Axel on 2017-05-11.
 */



/*effects for double navbars */
(function ($) {
  $(document).ready(function(){

    // hide .navbar first
    $(".second_navbar").hide();

    // fade in .navbar
    $(function () {
        $(window).scroll(function () {

                 // set distance user needs to scroll before we start fadeIn
            if ($(this).scrollTop() > 0) {
                $('.second_navbar').fadeIn();
            } else {
                $('.second_navbar').fadeOut();
            }
        });
    });

});
  }(jQuery));

/*effect for navbar*/
function openNav() {
    document.getElementById("mySidebar").style.width = "100%";
    document.getElementById("mySidebar").style.maxWidth = "700px";
    document.getElementById("mySidebar").style.display = "block";
}

function closeNav() {
    document.getElementById("mySidebar").style.display = "none";
}