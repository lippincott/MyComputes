//Infinite Scrolling
$(document).ready(function () {
  var infinite = new Waypoint.Infinite({
    element: $('.infinite-container')[0],
    onBeforePageLoad: function () {
      $('.loading').show();
      console.log('Loading')

    },
    onAfterPageLoad: function ($items) {
      $('.loading').hide();
      console.log('hidden')


      // Ajax Check To-Dos & Posts
      $("form[id^='make_checks_']").on('submit', function(e){
        var checks_area = this.id;

        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        const csrftoken = getCookie('csrftoken');
        console.log(csrftoken)


        function csrfSafeMethod(method) {
            // these HTTP methods do not require CSRF protection
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            }
        });


        e.preventDefault();
        e.stopImmediatePropagation();
        // alert('Hang on')
        $.ajax({
            type: $(this).attr('method'),
            url: this.action,
            data: $(this).serialize(),
            headers: {'X-CSRFToken': csrftoken },
            context: this,
            success: function(json, data, status) {
              // console.log('Favorites success 2')
              // document.getElementById(checks_area).reset();

              if (json.button == true) {
                $("#note_row"+json.post_pk).toggle( "slide" , function() {$("#note_row"+json.post_pk).remove();});
                  // $("#check_btn"+json.post_pk).replaceWith(`<div id="check_btn`+json.post_pk+`" class="note_check_btn"> <button title="Uncheck?" class="uncheck_note alert-success btn btn-link" type="submit" name="check_note_id" value="`+json.post_pk+`"><span class="material-icons">&#xe2e6;</span></button>`);
                  // alert("It's True")
              }

              if (json.button == false) {
                $("#note_row"+json.post_pk).toggle( "slide" ,  function() {$("#note_row"+json.post_pk).remove();});
                  // $("#check_btn"+json.post_pk).replaceWith(`<div id="check_btn`+json.post_pk+`" class="note_check_btn"> <button title="Check" class="check_note btn btn-link" type="submit" name="check_note_id" value="`+json.post_pk+`"><span class="material-icons">&#xe2e6;</span></button>`);
                  // alert("It's False")
              }

            },
            error : function(xhr,errmsg,err) {
            // provides a bit more info about the error to the console
            // console.log(xhr.status + ": " + xhr.responseText);
            console.log('ajax error')
            }
            });
            return false;
      });



      }

    });

});
