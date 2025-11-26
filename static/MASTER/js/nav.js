/**
 * Copyright 2021, Market Action Research
 * https://marketactionresearch.com
 * @author Market Action Research, Inc.
 * @desc Market Action Research, Inc. JS
 */
 $(document).ready(function(){
   $('#nav-icon1,#nav-icon2,#nav-icon3,#nav-icon4').click(function(){
     $(this).toggleClass('open');
   });
  // tooltips
  $(function () {
    $('[data-toggle="tooltip"]').tooltip()
  })
});
