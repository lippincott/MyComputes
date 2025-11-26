

// Ajax Records
$("form[id^='postForm1']").on('submit', function(e){

  // e.preventDefault();
  // e.stopImmediatePropagation();



  var mainsubmitbtn = $('#mainupload')
  var requestbtn = $('.firstvisible1')
  var loadingbtn = $('.secondvisible1')

  var mainformsection = $('#mainformsection')
  var advisory = $('#advisory ')
  var loadingbtn2 = $('.second_answersloading')


  requestbtn.hide();
  mainformsection.hide();
  loadingbtn.show().css({"display": "block", "margin": "auto", 'color':'#fff', 'width': '.75rem',});
  loadingbtn.parent().addClass('disabled')
  advisory.show().css({"display": "block", "margin": "auto",});
  loadingbtn2.show().css({"display": "block", "margin": "auto",});



  // alert('Hang on')
  console.log($(this).attr('method'));
  console.log(this.action);
  // console.log(formData);
  // console.log(csrftoken);

});
