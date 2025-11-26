/**
 * Copyright 2024, Market Action Research
 * https://marketactionresearch.com
 * @author Market Action Research, Inc.
 * @desc Market Action Research, Inc. JS
 */


// Enable Tooltips Everywhere
// var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
// var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
//   return new bootstrap.Tooltip(tooltipTriggerEl)
// })


// Ripple Effect
$(document).ready(function () {
    [].map.call(document.querySelectorAll('[anim="ripple"]'), el=> {
        el.addEventListener('click',e => {
            e = e.touches ? e.touches[0] : e;
            const r = el.getBoundingClientRect(), d = Math.sqrt(Math.pow(r.width,2)+Math.pow(r.height,2)) * 2;
            el.style.cssText = `--s: 0; --o: 1;`;  el.offsetTop;
            el.style.cssText = `--t: 1; --o: 0; --d: ${d}; --x:${e.clientX - r.left}; --y:${e.clientY - r.top};`
        })
    })
});


// Change notification Color & Display
$(document).ready(function () {

    // Load the Model with Tool Tip
    $(".modaltool").click(function() {
    var id = $(this)[0].attributes['data-bs-target'].value
    $(id).modal('show');
  });

  // Footer
  $("#mainfooter1").fadeIn('fast');



    // Back to top button
    var btn = $('#myBtn');
    // default
    btn.addClass('myUpBtn2');
    btn.removeClass('myUpBtn1');

    $(window).scroll(function() {
      if ($(window).width() >= 1){
          if ($(window).scrollTop() > 300) {
            btn.addClass('myUpBtn1');
            btn.removeClass('myUpBtn2');
            // console.log('showing')
          } else {
            btn.addClass('myUpBtn2');
            btn.removeClass('myUpBtn1');
            // console.log('hidden')
          }
      }
    });
    btn.on('click', function(e) {
      e.preventDefault();
      $('html, body').animate({scrollTop:0}, '300');
    });


    var svgBtn = document.querySelector("#myBtn > svg");

        if (svgBtn) {
            // Make scroll to top button increase height from bottom at bottom
            $(window).on('scroll', function() {
                var scrollBottom = $(document).height() - $(window).height() - $(window).scrollTop();
                // console.log(scrollBottom)
                if (scrollBottom < 100 && $(window).width() <= 991) {
                    svgBtn.style.bottom = '5.5rem'; //console.log("At Bottom")
                } else if ($(window).scrollTop() > 300 && scrollBottom < 100 && $(window).width() >= 991) {
                    svgBtn.style.bottom = '0.5rem';
                } else {
                    //pass
                }
            }).trigger('scroll');
        }


    new Date().getFullYear()
    if(document.getElementById("year")) {
      document.getElementById("year").innerHTML = new Date().getFullYear();
    }
    if(document.getElementById("year1")) {
      document.getElementById("year1").innerHTML = new Date().getFullYear();
    }
    if(document.getElementById("year2")) {
      document.getElementById("year2").innerHTML = new Date().getFullYear();
    }

});



$( document ).ready(function() {
  /**
   * Copyright 2021, Market Action Research
   * Licensed under the MIT license.
   * https://marketactionresearch.com
   * @author Market Action Research, Inc.
   * @desc Nav Customizations
   */

    window.onscroll = function() {
      growShrinkLogo()
    };

    $(window).resize(function() {
      growShrinkLogo()
    });


    function growShrinkLogo() {
      // var Top = document.getElementById("top_row1")
      var Logo = document.getElementById("mars_logo")
      var Ground = document.getElementById("mars_nav")
      var Fonts = document.querySelectorAll(".navbar-dark .navbar-nav .nav-link")
      var TopFonts = document.querySelectorAll(".top-left a")
      var TopButtons = document.querySelectorAll("a.the_top_buttons")
      var MobileWrapper = document.getElementById("mobile-mars-wrapper")

      if (document.body.scrollTop > 5 || document.documentElement.scrollTop > 5) {
        if ($(window).width() >= 991){
          // Logo.style.width = '40%';
          for (var i = 0; i < TopFonts.length; i++) {
          TopFonts[i].style.fontSize=".75rem";
          }
          for (var i = 0; i < TopButtons.length; i++) {
          TopButtons[i].style.fontSize=".63rem";
          TopButtons[i].style.letterSpacing=".1rem";
          }
        } else {
          // Small Screens
          // Logo.style.width = '55%';
          for (var i = 0; i < TopFonts.length; i++) {
          TopFonts[i].style.fontSize=".75rem";
          }
          for (var i = 0; i < TopButtons.length; i++) {
          TopButtons[i].style.fontSize=".63rem";
          TopButtons[i].style.letterSpacing=".1rem";
          }
        }
        Logo.style.marginTop='0rem';
        Logo.style.padding = '0.1rem';
        Ground.style.background = '#ffffffd4';
        // MobileWrapper.style.marginTop='0rem';

        for (var i = 0; i < Fonts.length; i++) {
        // Fonts[i].style.fontSize=".9rem";
        // Fonts[i].style.letterSpacing=".03rem";
        Fonts[i].classList.add("navfonts1");
        Fonts[i].classList.remove("navfonts2");
        }

      } else {

        if ($(window).width() >= 991){
          // Logo.style.width = '100%';
          for (var i = 0; i < TopFonts.length; i++) {
          TopFonts[i].style.fontSize="1rem";
          }
          for (var i = 0; i < TopButtons.length; i++) {
          TopButtons[i].style.fontSize=".85rem";
          TopButtons[i].style.letterSpacing="normal";
          }
        } else {
          // Small Screens
          // Logo.style.width = '69%';
          for (var i = 0; i < TopFonts.length; i++) {
          TopFonts[i].style.fontSize=".8rem";
          }
          for (var i = 0; i < TopButtons.length; i++) {
          TopButtons[i].style.fontSize=".8rem";
          TopButtons[i].style.letterSpacing="normal";
          }
        }
        Logo.style.marginTop='0.5rem';
        Logo.style.padding = '0.5rem';
        Ground.style.background = '#fff';
        // MobileWrapper.style.marginTop='1rem';

        for (var i = 0; i < Fonts.length; i++) {
        // Fonts[i].style.fontSize=".85rem";
        // Fonts[i].style.letterSpacing="normal";
        Fonts[i].classList.add("navfonts2");
        Fonts[i].classList.remove("navfonts1");
        }
      }
    }
    });


$( document ).ready(function() {

  $("[id^='show_content']").fadeIn();
  $(".show_content").fadeIn();


  var mainsubmitbtn = $('#mainsubmit')
  var requestbtn = $('.firstvisible')
  var loadingbtn = $('.secondvisible')


  mainsubmitbtn.on('click', function(e){
    // e.preventDefault();

    requestbtn.hide();
    loadingbtn.show().css({"display": "block", "margin": "auto", 'color':'#fff', 'width': '.75rem',});
    // $('span.secondvisible').parent().prop('disabled', true);
    // $('span.firstvisible').parent().prop('disabled', true);
    loadingbtn.parent().addClass('disabled')
    // TIMEOUT FUNCTION TO RESTORE BUTTON
    setTimeout(function(){
      requestbtn.fadeIn();
      loadingbtn.hide();
      loadingbtn.parent().removeClass('disabled')
    }, 5000);
  })

});



$(document).ready(function(){
    // Event for pushed the video
    $('#MARScarousel1').carousel({
        pause: true,
        interval: false
    });
});





$( document ).ready(function() {
    $("[id^='showtime']").fadeIn();
    $("[class='showtime']").fadeIn();
    // Converts UTC date time to local time
     // $(".date").toArray().map(function(i){
     //    i.replaceWith(new Date(i.innerText).toDateString() + ' ' + new Date(i.innerText).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }))
     //  });
     $(".date").toArray().map(function(i){
        var date = new Date(i.innerText);
        var date = new Date(inner1);
        var formattedDate = date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
        var formattedTime = date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true });
        i.replaceWith(formattedDate + ' ' + formattedTime);
      });
      $(".date1").toArray().map(function(i){
         i.replaceWith(new Date(i.innerText).toLocaleDateString() + ' ' + new Date(i.innerText).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }))
       });
      // Formats as mm/dd/yyyy
      $(".date2").toArray().map(function(i){
         i.replaceWith(new Date(i.innerText).toLocaleDateString())
       });
       $(".date3").toArray().map(function(i){
          i.replaceWith(new Date(i.innerText).toLocaleDateString())
        });


        $(".date4").each(function() {
            var isoDateString = $(this).text().trim();

            // Check if the date string is valid
            if (isoDateString) {
                try {
                    // Convert the ISO date string to a JavaScript Date object
                    var date = new Date(isoDateString);

                    if (!isNaN(date.getTime())) {
                        // Function to pad single digit numbers with a leading zero
                        function pad(number) {
                            return (number < 10 ? '0' : '') + number;
                        }

                        // Format the date as MM/DD/YYYY
                        var formattedDate = pad(date.getMonth() + 1) + '/' + pad(date.getDate()) + '/' + date.getFullYear();

                        // Format the time as HH:MM AM/PM
                        var formattedTime = date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit', hour12: true });

                        // Update the time element with the formatted date and time
                        $(this).text(formattedDate + ' ' + formattedTime);
                    } else {
                        console.error("Invalid date:", isoDateString);
                        $(this).text("Invalid Date");
                    }
                } catch (e) {
                    console.error("Error parsing date:", e);
                    $(this).text("Error");
                }
            } else {
                console.error("No date string found.");
                $(this).text("No Date");
            }
        });



});

// Loads anytime ajax is executed
$( document ).ajaxComplete(function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl)
    })

    $("[id^='showtime']").fadeIn();
  // Converts UTC date time to local time
    $(".date").toArray().map(function(i){
      i.replaceWith(new Date(i.innerText).toDateString() + ' ' + new Date(i.innerText).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }))
    });
    $(".date2").toArray().map(function(i){
       i.replaceWith(new Date(i.innerText).toLocaleDateString())
     });
});



$(document).ready(function(){
  /**
   * Copyright 2021, Market Action Research
   * Licensed under the MIT license.
   * https://marketactionresearch.com
   * @author Market Action Research, Inc.
   * @desc Vid Loader
   */

    // Create an Array of Video Ids
    var videoId = $("[id^='id_tube_url']").map(function () { return $(this).val(); }).get();

    // create list of expressions youtube
    var regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
    // vimeo
    var v_regExp = /^.*(vimeo.com\/)([^#\&\?]*).*/;

    // create array of videos
    var video_pk =$("[id^='id_tube_url']").toArray();

    for(let i = 0; i < video_pk.length; i++){

        var video_id = video_pk[i].id
        // console.log(video_id);

        var myId = video_pk[i].value
        // console.log(myId);

        var match = myId.match(regExp)
        var v_match = myId.match(v_regExp)
        // console.log(v_match)

        if (match != null && match[2].length == 11) {
            $('#' + video_id).replaceWith('<pre class="my_VideoYou"><iframe title="YouTube Video"  width="100%" src="https://www.youtube.com/embed/' + match[2] + '" frameborder="0" allowfullscreen></iframe></pre>');
        }

        if (v_match != null && v_match[2].length == 9 || v_match[2].length == 8) {
            $('#' + video_id).replaceWith('<pre class="my_VideoYou"><iframe title="Vimeo Video" width="100%" src="https://player.vimeo.com/video/' + v_match[2]  + '" frameborder="0" allowfullscreen></iframe>');
         }

    }

});


$(document).ready(function(){
  /**
   * Copyright 2024, Market Action Research
   * Licensed under the MIT license.
   * https://marketactionresearch.com
   * @author Market Action Research, Inc.
   * @desc Button Mouseover
   */

    // On button mouseover
    $("[id^='cta-b']").mouseover(function(){ //button
        var button_id = this.id;
        var the_b_id = button_id.replace('cta-b' , '')
        var the_i_id = '#cta-i'+the_b_id
        $(the_i_id).trigger('mouseover');// image
    });

    $("[id^='cta-b']").mouseout(function(){ //button
        var button_id = this.id;
        var the_b_id = button_id.replace('cta-b' , '')
        var the_i_id = '#cta-i'+the_b_id
        $(the_i_id).trigger('mouseout'); // image
    });


    $("[id^='cta-i']").mouseover(function(){ //button
        var button_id = this.id;
        var the_i_id = button_id.replace('cta-i' , '')
        var the_b_id = '#cta-b'+the_i_id
        $(the_b_id).addClass('manual-ripple-style');// image
    });

    $("[id^='cta-i']").mouseout(function(){ //button
        var button_id = this.id;
        var the_i_id = button_id.replace('cta-i' , '')
        var the_b_id = '#cta-b'+the_i_id
        $(the_b_id).removeClass('manual-ripple-style');// image
    });

});

// fadeIN

$( document ).ready(function() {
  $(".show_content").fadeIn();
});


// Slide-up Boxes
    $(document).ready(function(){


  /**
   * Copyright 2021, Market Action Research
   * Licensed under the MIT license.
   * https://marketactionresearch.com
   * @author Market Action Research, Inc.
   * @desc Checks if elements are within the vertical
   *       position of user viewport of browser
   */

  $.fn.visible = function(partial) {

      var $t            = $(this),
          $w            = $(window),
          viewtheTop       = $w.scrollTop(),
          viewtheBottom    = viewtheTop + $w.height(),
          _top          = $t.offset().top,
          _bottom       = _top + $t.height(),
          compTop    = partial === true ? _bottom : _top,
          compBottom = partial === true ? _top : _bottom;

    return ((compBottom <= viewtheBottom) && (compTop >= viewtheTop));

  };

  var win = $(window);

  var allMods = $(".comeon-up");

  allMods.each(function(i, el) {
    var el = $(el);
    if (el.visible(true)) {
      el.addClass("already-visible");
    }
  });

  win.scroll(function(event) {

    allMods.each(function(i, el) {
      var el = $(el);
      if (el.visible(true)) {
        el.addClass("make-visible");
      }
    });

  });


});
