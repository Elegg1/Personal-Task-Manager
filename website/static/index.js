$(function() {
    let navbar = $('.navbar');
    let navbarHeight = navbar.height();
     
    $(window).scroll(function() {
      if($(this).scrollTop() > 1) {
       navbar.addClass('navbar-fixed');
       $('body').css({
          'paddingTop': navbarHeight+'px'
       });
      } else {
        navbar.removeClass('navbar-fixed');
       $('body').css({
        'paddingTop': 0
       })
      }
    });
   });


function deleteTask(taskId){
    $(window).unbind('beforeunload');
    fetch('/delete-task', {
        method: 'POST',
        body: JSON.stringify({taskId: taskId})
    }).then((_res) => {
        window.location.href='/';
    });
}