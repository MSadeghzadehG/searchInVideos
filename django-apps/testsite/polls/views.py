from django.http import HttpResponse
from django.template import loader
from .models import Video
from .models import Subtitle


# Create your views here.


def index(request, word):
    template = loader.get_template('index.html')
    subtitle_list = Subtitle.objects.order_by('subtitleLanguage')
    videos_list = []
    playlist = []

    if word == 'null':
        videos_list = Video.objects.order_by('name')
    else:
        videos_list = search(word, subtitle_list)

    for video in videos_list:
        if not (video.name in [video1.name for video1 in playlist]):
            playlist.append(video)
    context = {'playlist': playlist, 'videos': videos_list, 'subtitles': subtitle_list, 'selectedVideo': videos_list[0]}
    return HttpResponse(template.render(context, request))


def search(word, subtitles):
    return []



