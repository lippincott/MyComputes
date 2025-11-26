
// $( document ).ready(function() {
//   closeNav()
// });


// document.getElementById('myToggle').addEventListener('click', function () {
//   var collapseElement = document.getElementById('nav-icon3');
//   var bsCollapse = new bootstrap.Collapse(collapseElement, {
//     toggle: false
//   });
//   bsCollapse.toggle();
//   console.log('triggered')
// });
//
//
// function openNav() {
//   $("#mySidenav").animate({width: '320px'}, 10)
//   $("#main").animate({marginLeft: '320px'}, 10);
//       setTimeout(function(){
//       $(".sidenav-link").fadeIn('fast');
//       }, 300);
//   console.log('opennav')
// }
//
// function closeNav() {
//   $("#mySidenav").animate({width: '0'}, 100)
//   $("#main").animate({marginLeft: '0'}, 100);
//   $(".sidenav-link").hide();
//   // For Bootstrap Trigger
//   $("#nav-icon3").removeClass("open");
//   $("#nav-icon3").addClass("collapse");
//   console.log('closenav')
// }


//
// var isNavOpen = false;
//
// document.getElementById('nav-icon32').addEventListener('click', function () {
//     openNav();
//     isNavOpen = true;
// });
//
// document.getElementById('myToggle').addEventListener('click', function () {
//     closeNav();
//     isNavOpen = false;
//
// });
//
// document.getElementById('closeBtn').addEventListener('click', function (event) {
//   closeNav();
//   isNavOpen = false;
// });
//
// // onclick="openNav()"
// function openNav() {
//   $("#mySidenav").animate({width: '320px'}, 10)
//   $("#main").animate({marginLeft: '320px'}, 10);
//       setTimeout(function(){
//       $(".sidenav-link").fadeIn('fast');
//       }, 300);
//   isNavOpen = true;
//   console.log('opennav');
// }
//
// function closeNav() {
//     $("#mySidenav").animate({width: '0'}, 100)
//     $("#main").animate({marginLeft: '0'}, 100);
//     $(".sidenav-link").hide();
//     isNavOpen = false;
//     console.log('closenav');
//   };
//


  $( document ).ready(function() {
    closeNav()
  });

  function openNav() {
    $('#admin-dash1').hide();
    $("#mySidenav").animate({width: '250px'}, 10)
    $("#main").animate({marginLeft: '250px'}, 10);
        setTimeout(function(){
        $(".sidenav-link").fadeIn('fast');
        }, 300);

  }

  function closeNav() {
    $("#mySidenav").animate({width: '0'}, 100)
    $("#main").animate({marginLeft: '0'}, 100);
    $(".sidenav-link").hide();
    $('#admin-dash1').show();
  }
