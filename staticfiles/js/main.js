
        $(document).ready(function () {
            // Smooth scrolling for anchor links
            $('a.nav-link').on('click', function (event) {
                if (this.hash !== "") {
                    event.preventDefault();

                    var hash = this.hash;

                    $('html, body').animate({
                        scrollTop: $(hash).offset().top
                    }, 300, function () {
                        window.location.hash = hash;
                    });
                }
            });


            // Show or hide the scroll-to-top button based on the user's scroll position
            $(window).scroll(function () {
                if ($(this).scrollTop() > 100) {
                    $('#scrollToTopBtn').fadeIn();
                } else {
                    $('#scrollToTopBtn').fadeOut();
                }
            });

            // Scroll to top when the button is clicked
            $('#scrollToTopBtn').click(function () {
                $('html, body').animate({ scrollTop: 0 }, 800);
            });
        });

 
