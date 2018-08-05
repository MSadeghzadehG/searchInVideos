document.addEventListener('DOMContentLoaded', () => { 
  // This is the bare minimum JavaScript. You can opt to pass no arguments to setup.
  const player = new Plyr('#player');



var reply_click = function()
{
    console.log('omad');
}

for (let index in document.getElementsByClassName('playlist-item').length){
    console.log(index);
    document.getElementById('item-'+index).onclick = reply_click;
}

$('.playlist-item').click(function () {
    // var pre = $(this).id;
    // console.log(pre);
    // var list = pre.split('-');
    // console.log(list)
    $.ajax({
        url : 'http://localhost:8000/ajax/',
        success: function(data){
            console.log('clicked');
            let video = data[0].fields;
            // console.log(JSON.stringify(video))
            player.currentTime = 10;

        }
    });
});








// The small arrow that marks the active search icon:
// var arrow = $('<span>',{className:'arrow'}).appendTo('ul.search-icons');
//
// $('ul.search-icons li').click(function(){
//     var el = $(this);
//
//     if(el.hasClass('active')){
//         // The icon is already active, exit
//         return false;
//     }
//
//     el.siblings().removeClass('active');
//     el.addClass('active');
//
//     // Move the arrow below this icon
//     arrow.stop().animate({
//         left        : el.position().left,
//         marginLeft  : (el.width()/2)-4
//     });
//
// });
//
// // Marking the web search icon as active:
// $('li.t10').click();
//
// // Focusing the input text box:
// $('#s').focus();
//
// $('#searchForm').submit(function(){
//     googleSearch();
//     return false;
// });



});
