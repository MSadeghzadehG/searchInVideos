document.addEventListener('DOMContentLoaded', () => { 
  // This is the bare minimum JavaScript. You can opt to pass no arguments to setup.
  const player = new Plyr('#player');

// The small arrow that marks the active search icon:
var arrow = $('<span>',{className:'arrow'}).appendTo('ul.search-icons');

$('ul.search-icons li').click(function(){
    var el = $(this);

    if(el.hasClass('active')){
        // The icon is already active, exit
        return false;
    }

    el.siblings().removeClass('active');
    el.addClass('active');

    // Move the arrow below this icon
    arrow.stop().animate({
        left        : el.position().left,
        marginLeft  : (el.width()/2)-4
    });

});

// Marking the web search icon as active:
$('li.t10').click();

// Focusing the input text box:
$('#s').focus();

$('#searchForm').submit(function(){
    googleSearch();
    return false;
});



});
