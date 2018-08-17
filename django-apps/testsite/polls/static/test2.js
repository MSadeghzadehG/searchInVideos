document.addEventListener('DOMContentLoaded', () => {


    // let server_url = 'http://91.98.76.233/';
    let server_url = 'http://localhost:8000/';

    const player = new Plyr('#player');


    function stripEndQuotes(s){
            var t=s.length;
            if (s.charAt(0)=='"') s=s.substring(1,t--);
            if (s.charAt(--t)=='"') s=s.substring(0,t);
            return s;
        }

    document.getElementById('searchbar-button').onclick = function () {
      $("#list-container").empty();
      let searchedWord = document.getElementById('searchbar-input').value;
      let time = (parseInt(document.getElementsByClassName('active')[0].id)/10).toString();
      console.log(time);
      $.ajax({
          url: server_url + 'ajax/'+searchedWord+'/'+time,
          success: function (data) {
              // console.log('clicked');
              console.log(Object.keys(data).length)
              createPlayList(data);
              if (Object.keys(data).length > 0) {
                  for (let i in data) {
                      setPlayerSource(data[i]);
                      break;
                  }
              }
          }
      });
    };

    function setPlayerSource(data) {
        console.log(data)
        $.ajax({
            url: server_url+ 'video_ajax/',
            type: 'POST',
            contentType:'application/json',
            data : JSON.stringify(data) + "[]" +JSON.stringify(data.subtitle) + "[]" + JSON.stringify(data.video),
            success: function () {
                player.source = {
                    type: 'video',
                    sources: [
                        {
                            // src: data.video.videoPath + "#t=" + data.startTime + ',' + data.endTime,
                            src: data.video.videoPath,
                            type: data.video.videoFormat,
                            size: data.video.videoQuality,
                        },
                    ],
                    poster: 'https://envideo.ir/wp-content/uploads/2017/12/envideo-logo-300x83.png',
                    tracks: [
                        {
                            default: true,
                            kind: 'captions',
                            label: capitalizeFirstLetter(data.subtitle.subtitleLanguage),
                            srclang: data.subtitle.subtitleLanguage,
                            src: data.subtitle.subtitlePath,
                        },
                    ],
                };
            }
        });

        function capitalizeFirstLetter(string) {
           return string.charAt(0).toUpperCase() + string.slice(1);
        }
    }

    function createPlayList(data) {
        var list = document.createElement("DIV");
        list.id = "playlist";
        list.class = "playlist";
        document.getElementById('list-container').append(list);
        for (let i in data) {
            var node = document.createElement("DIV");
            var title = document.createElement("H4");
            var time = document.createElement("H6");
            title.innerHTML = '• ' + stripEndQuotes(JSON.stringify(data[i].video.name));
            time.innerHTML = stripEndQuotes(JSON.stringify(data[i].startTime))+'-'+stripEndQuotes(JSON.stringify(data[i].endTime));
            title.classList.toggle("text-left")
            title.classList.toggle("col-sm-4")
            time.classList.toggle("text-right")
            title.classList.toggle("col-sm-8")
            node.id = "item-" + data[i].id;
            node.classList.toggle("playlist-item");
            document.getElementById('playlist').appendChild(node);
            document.getElementById("item-" + data[i].id).appendChild(title);
            document.getElementById("item-" + data[i].id).appendChild(time);
            document.getElementById("item-" + data[i].id).onclick = function () { setPlayerSource(data[i]) };
            // document.getElementById('item-' + data[i].id)..
        }
    }


    $('ul.icons li').click(function(){
        var el = $(this);

        if(el.hasClass('active')){
            // The icon is already active, exit
            return false;
        }
        el.siblings().removeClass('active');
        el.addClass('active');
    });

});
