Array.from(
  document.querySelectorAll('.element'),
  function(el){

    el.addEventListener('mousemove',function(e){
      el.style.setProperty('--px', e.clientX - el.offsetLeft);
      el.style.setProperty('--py', e.clientY - el.offsetTop);
    });

  });
